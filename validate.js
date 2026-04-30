const fs = require('fs');

// ==========================================
// НАСТРОЙКИ LLM API
// ==========================================
const LLM_CONFIGS = {
    deepseek: {
        url: 'https://api.deepseek.com/chat/completions',
        key: 'xxx',
        model: 'deepseek-chat'
    },
    gemini: {
        url: 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
        key: 'xxx',
        model: 'gemini-2.5-flash'
    }
};

// ==========================================
// ПРОМПТЫ
// ==========================================
const SYSTEM_MESSAGE = `You are an AI assistant specialized in comparing and mapping steps in business processes. Your task is to analyze the ground truth steps and the response steps for a given business process activity, determine the best mappings between steps based on semantic similarity, and provide a structured output of the relationships. Follow these guidelines:

1. Step Matching: Compare each ground truth step with each response step. Determine best matches based on semantic similarity. Group steps if granularity differs.
2. Matching Criteria (Assign one of these to each match):
    - Identical Match: Steps are identical or nearly identical in wording and meaning.
    - Functional Equivalence: Steps describe the same action/outcome using different words.
    - Granularity Difference: Steps share common elements but differ in scope (one step encompasses multiple).
    - No Match: Steps do not correspond to each other.
3. Output Structure: Provide analysis strictly in JSON format:
{
    "activity_name": "Name",
    "step_mappings": [
        {
            "ground_truth_steps": [{"step_number": 1, "description": "..."}],
            "response_steps": [{"step_number": 1, "description": "..."}],
            "match_type": "Identical Match" | "Functional Equivalence" | "Granularity Difference" | "No Match",
            "confidence": 85,
            "explanation": "..."
        }
    ],
    "unmatched_ground_truth_steps": [{"step_number": 2, "description": "...", "reason": "..."}],
    "unmatched_response_steps": [{"step_number": 3, "description": "...", "reason": "..."}]
}`;

const generateUserMessage = (groundTruth, response) => `
Compare the following ground truth activity and substeps with the response activity and substeps. 
Provide a detailed mapping in the JSON format specified in the system message.

Ground Truth:
${JSON.stringify(groundTruth, null, 2)}

Response:
${JSON.stringify(response, null, 2)}
`;

// ==========================================
// ФУНКЦИЯ НЕЧЁТКОГО СРАВНЕНИЯ (Levenshtein Distance)
// ==========================================
function levenshteinDistance(a, b) {
    const matrix = [];
    for (let i = 0; i <= b.length; i++) matrix[i] = [i];
    for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
    
    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i-1) === a.charAt(j-1)) {
                matrix[i][j] = matrix[i-1][j-1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i-1][j-1] + 1,
                    matrix[i][j-1] + 1,
                    matrix[i-1][j] + 1
                );
            }
        }
    }
    return matrix[b.length][a.length];
}

function similarity(a, b) {
    const longer = a.length > b.length ? a : b;
    const shorter = a.length > b.length ? b : a;
    if (longer.length === 0) return 1.0;
    const distance = levenshteinDistance(longer, shorter);
    return (longer.length - distance) / longer.length;
}

// Функция поиска активности с нечётким сопоставлением
function findActivityFuzzy(activityName, predictions, threshold = 0.85) {
    // Сначала пробуем точное совпадение
    const exact = predictions.find(pa => pa.activity_name === activityName);
    if (exact) return exact;
    
    // Если не нашли — ищем нечётко
    let bestMatch = null;
    let bestScore = 0;
    
    for (const pred of predictions) {
        const score = similarity(activityName, pred.activity_name);
        if (score > bestScore && score >= threshold) {
            bestScore = score;
            bestMatch = pred;
        }
    }
    
    if (bestMatch) {
        console.log(`🔍 Нечёткое совпадение: "${activityName}" → "${bestMatch.activity_name}" (score: ${bestScore.toFixed(3)})`);
    }
    
    return bestMatch;
}

// ==========================================
// ФУНКЦИЯ ОЧИСТКИ ОТВЕТА
// ==========================================
function parseLLMResponse(text) {
    try {
        const cleaned = text.replace(/```json/gi, '').replace(/```/g, '').trim();
        const start = cleaned.indexOf('{');
        const end = cleaned.lastIndexOf('}');
        if (start === -1 || end === -1) throw new Error("JSON не найден в ответе");
        return JSON.parse(cleaned.substring(start, end + 1));
    } catch (error) {
        console.error("❌ Ошибка парсинга JSON от судьи. Сырой ответ:\n", text);
        throw error;
    }
}

// ==========================================
// ФУНКЦИЯ ВЫЗОВА LLM
// ==========================================
async function callLLM(groundTruthActivity, responseActivity, judgeConfig) {
    const userMessage = generateUserMessage(groundTruthActivity, responseActivity);

    const response = await fetch(judgeConfig.url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${judgeConfig.key}`
        },
        body: JSON.stringify({
            model: judgeConfig.model,
            messages: [
                { role: "system", content: SYSTEM_MESSAGE },
                { role: "user", content: userMessage }
            ],
            temperature: 0.1
        })
    });

    if (!response.ok) {
        const err = await response.text();
        throw new Error(`API Error: ${response.status} - ${err}`);
    }

    const data = await response.json();
    const rawContent = data.choices?.[0]?.message?.content;
    if (!rawContent) throw new Error("Пустой ответ от модели-судьи");
    
    return parseLLMResponse(rawContent);
}

// ==========================================
// ФУНКЦИЯ ЛОГИРОВАНИЯ ДЕТАЛЬНЫХ РЕЗУЛЬТАТОВ
// ==========================================
function saveDetailedLog(modelName, activityName, llmResult, error = null) {
    const logDir = './validation_logs';
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${logDir}/mapping_${modelName}_${activityName.replace(/[^a-z0-9]/gi, '_')}_${timestamp}.json`;
    
    const logEntry = {
        timestamp,
        activity_name: activityName,
        model: modelName,
        error: error ? error.message : null,
        llm_result: llmResult
    };
    
    fs.writeFileSync(filename, JSON.stringify(logEntry, null, 2), 'utf8');
    return filename;
}

// ==========================================
// ЛОГИКА СРАВНЕНИЯ И ПОДСЧЕТА МЕТРИК
// ==========================================
async function evaluateFile(truthPath, predictionPath, modelName, judgeConfig) {
    console.log(`\n⏳ Анализ файла ${predictionPath} (Судья: ${judgeConfig.model})...`);
    
    if (!fs.existsSync(truthPath)) {
        console.error(`❌ Файл эталона ${truthPath} не найден!`);
        return;
    }
    if (!fs.existsSync(predictionPath)) {
        console.error(`❌ Файл предсказания ${predictionPath} не найден!`);
        return;
    }

    const truthData = JSON.parse(fs.readFileSync(truthPath, 'utf8'));
    const predictionData = JSON.parse(fs.readFileSync(predictionPath, 'utf8'));

    let totalGtSteps = 0;
    let totalPredSteps = 0;
    
    const metrics = {
        'Identical Match': 0,
        'Functional Equivalence': 0,
        'Granularity Difference': 0,
        'No Match': 0,
        'Extra (Unmatched Response)': 0
    };

    // Сбор детальной статистики для отладки
    const detailedStats = {
        matched_by_exact: 0,
        matched_by_fuzzy: 0,
        not_found: 0,
        mappings: []
    };

    for (const gtActivity of truthData) {
        // Используем нечёткое сопоставление вместо строгого ===
        const predActivity = findActivityFuzzy(gtActivity.activity_name, predictionData, 0.85);
        totalGtSteps += gtActivity.substeps.length;

        if (!predActivity) {
            console.warn(`⚠️ Активность "${gtActivity.activity_name}" не найдена в предсказании (даже с нечётким поиском)`);
            metrics['No Match'] += gtActivity.substeps.length;
            detailedStats.not_found++;
            // Логируем отсутствие активности
            saveDetailedLog(modelName, gtActivity.activity_name, null, new Error("Activity not found in prediction"));
            continue;
        }

        // Отслеживаем, как было найдено совпадение
        if (predActivity.activity_name === gtActivity.activity_name) {
            detailedStats.matched_by_exact++;
        } else {
            detailedStats.matched_by_fuzzy++;
        }

        totalPredSteps += predActivity.substeps.length;

        try {
            const llmResult = await callLLM(gtActivity, predActivity, judgeConfig);
            
            // Сохраняем детальный лог маппинга
            saveDetailedLog(modelName, gtActivity.activity_name, llmResult);
            
            if (llmResult.step_mappings) {
                llmResult.step_mappings.forEach(mapping => {
                    const stepCount = mapping.ground_truth_steps?.length || 1;
                    const type = mapping.match_type;
                    
                    if (metrics[type] !== undefined) {
                        metrics[type] += stepCount;
                    } else {
                        metrics['No Match'] += stepCount;
                    }
                    
                    // Добавляем в статистику для отладки
                    detailedStats.mappings.push({
                        activity: gtActivity.activity_name,
                        match_type: type,
                        gt_steps: mapping.ground_truth_steps?.map(s => s.description),
                        resp_steps: mapping.response_steps?.map(s => s.description),
                        confidence: mapping.confidence,
                        explanation: mapping.explanation
                    });
                });
            }

            if (llmResult.unmatched_ground_truth_steps) {
                metrics['No Match'] += llmResult.unmatched_ground_truth_steps.length;
            }

            if (llmResult.unmatched_response_steps) {
                metrics['Extra (Unmatched Response)'] += llmResult.unmatched_response_steps.length;
            }

        } catch (error) {
            console.error(`❌ Ошибка при обработке активности "${gtActivity.activity_name}":`, error.message);
            saveDetailedLog(modelName, gtActivity.activity_name, null, error);
            metrics['No Match'] += gtActivity.substeps.length;
        }
    }

    printReport(modelName, metrics, totalGtSteps, totalPredSteps, detailedStats);
}

// ==========================================
// ВЫВОД РЕЗУЛЬТАТОВ + МЕТРИКА COVERAGE
// ==========================================
function printReport(modelName, metrics, totalGtSteps, totalPredSteps, detailedStats) {
    const totalAssessed = totalGtSteps + metrics['Extra (Unmatched Response)'];
    
    // Метрика Coverage: какой % эталонных шагов был хоть как-то распознан
    const coverage = totalGtSteps > 0 
        ? ((totalGtSteps - metrics['No Match']) / totalGtSteps * 100).toFixed(2) 
        : "0.00";
    
    const lines = [];

    lines.push(`\n=================================================`);
    lines.push(`📊 РЕЗУЛЬТАТЫ ДЛЯ: ${modelName.toUpperCase()}`);
    lines.push(`=================================================`);
    lines.push(`Всего шагов в эталоне: ${totalGtSteps}`);
    lines.push(`Всего шагов сгенерировано: ${totalPredSteps}`);
    lines.push(`🎯 Coverage (распознано эталона): ${coverage}%\n`);

    Object.keys(metrics).forEach(key => {
        const count = metrics[key];
        const percentage = totalAssessed > 0 ? ((count / totalAssessed) * 100).toFixed(2) : "0.00";
        const line = `- ${key.padEnd(28)} : ${count} (${percentage}%)`;
        lines.push(line);
        console.log(line);
    });
    
    // Статистика сопоставления активностей
    lines.push(`\n🔍 Статистика сопоставления активностей:`);
    lines.push(`   - Найдено точно: ${detailedStats.matched_by_exact}`);
    lines.push(`   - Найдено нечётко: ${detailedStats.matched_by_fuzzy}`);
    lines.push(`   - Не найдено: ${detailedStats.not_found}`);
    console.log(lines[lines.length - 1]);
    
    lines.push(`=================================================\n`);
    console.log(lines[lines.length - 1]);

    // Сохраняем в файл
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `report_${modelName}_${timestamp}.txt`;
    fs.writeFileSync(filename, lines.join('\n'), 'utf8');
    console.log(`💾 Отчет сохранен в ${filename}`);
    console.log(`📁 Детальные логи маппингов: ./validation_logs/`);
}

// 🆕 ==========================================
// ФУНКЦИЯ ЗАДЕРЖКИ (для предотвращения 503 ошибок)
// ==========================================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// ==========================================

// ==========================================
// ЗАПУСК
// ==========================================
async function run() {
    const truthFile = './ground_truth.json';
    
    // ЕДИНЫЙ СУДЬЯ: Используем Gemini для проверки обоих файлов
    const judge = LLM_CONFIGS.gemini; 

    console.log("🚀 Запуск оценки с улучшенной валидацией...");

    // Оцениваем работу Google
    await evaluateFile(truthFile, './prediction_google.json', 'Google', judge);

    // 🆕 ==========================================
    // ЗАДЕРЖКА 12 СЕКУНД перед вызовом DeepSeek API
    // (для предотвращения 503 ошибки rate limiting)
    // ==========================================
    console.log("\n⏳ Ожидание 12 секунд для соблюдения лимитов API...");
    await sleep(12000);
    // ==========================================

    // Оцениваем работу DeepSeek
    await evaluateFile(truthFile, './prediction_deepseek.json', 'DeepSeek', judge);
    
    console.log("✅ Все сравнения успешно завершены!");
}

run();