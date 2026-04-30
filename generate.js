const fs = require('fs');

const LLM_CONFIGS = {
    deepseek: {
        url: 'https://api.deepseek.com/chat/completions',
        key: 'xxxx',
        model: 'deepseek-chat'
    },
    gemini: {
        url: 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
        key: 'xxx',
        model: 'gemini-2.5-flash'
    }
};

const SYSTEM_PROMPT = `You are a strict JSON executor. Follow the user's JSON instructions exactly. Return ONLY valid JSON. Do not use markdown, backticks, or conversational text.`;

function parseLLMResponse(text) {
    try {
        const start = text.indexOf('{');
        const end = text.lastIndexOf('}');
        if (start === -1 || end === -1) throw new Error("JSON объект не найден");
        return JSON.parse(text.substring(start, end + 1));
    } catch (error) {
        console.error("❌ Ошибка парсинга JSON. Сырой ответ:\n", text);
        throw error;
    }
}

// 🆕 ==========================================
// ФУНКЦИЯ ЗАДЕРЖКИ (для предотвращения 503 ошибок)
// ==========================================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// ==========================================

async function generatePrediction(config, promptData, outputFileName, modelName) {
    console.log(`\n⏳ Отправка задачи в ${modelName}...`);
    const userMessage = `${JSON.stringify(promptData, null, 2)}\n\nСтарт`;

    try {
        const response = await fetch(config.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${config.key}`
            },
            body: JSON.stringify({
                model: config.model,
                messages: [
                    { role: "system", content: SYSTEM_PROMPT },
                    { role: "user", content: userMessage }
                ],
                temperature: 0.1
            })
        });

        if (!response.ok) {
            const err = await response.text();
            throw new Error(`API Error ${response.status}: ${err}`);
        }

        const data = await response.json();
        const rawContent = data.choices?.[0]?.message?.content;
        if (!rawContent) throw new Error("Пустой ответ от модели");

        let parsedJson = parseLLMResponse(rawContent);

        // 🔧 Fallback: если модель проигнорировала обёртку и вернула просто массив
        if (Array.isArray(parsedJson)) {
            console.log(`⚠️ ${modelName} вернул массив вместо объекта. Автоматическая обёртка...`);
            parsedJson = { decomposition_result: parsedJson };
        }

        if (!parsedJson.decomposition_result) {
            throw new Error(`Отсутствует ключ "decomposition_result". Получено: ${Object.keys(parsedJson).join(', ')}`);
        }

        fs.writeFileSync(outputFileName, JSON.stringify(parsedJson.decomposition_result, null, 2), 'utf8');
        console.log(`✅ Файл ${outputFileName} успешно сгенерирован моделью ${modelName}!`);

    } catch (error) {
        console.error(`❌ Ошибка при генерации ${modelName}:`, error.message);
    }
}

async function runGeneration() {
    const promptFile = './prompt.json';
    if (!fs.existsSync(promptFile)) {
        console.error(`❌ Файл ${promptFile} не найден!`);
        return;
    }

    const promptData = JSON.parse(fs.readFileSync(promptFile, 'utf8'));
    console.log("🚀 Запуск автоматической генерации разбиений...");

    // 1. Генерируем ответ от DeepSeek
    await generatePrediction(LLM_CONFIGS.deepseek, promptData, './prediction_deepseek.json', 'DeepSeek');

    // 🆕 ==========================================
    // ЗАДЕРЖКА 12 СЕКУНД перед вызовом Google API
    // (для предотвращения 503 ошибки rate limiting)
    // ==========================================
    console.log("\n⏳ Ожидание 12 секунд для соблюдения лимитов Google API...");
    await sleep(12000);
    // ==========================================

    // 2. Генерируем ответ от Google
    await generatePrediction(LLM_CONFIGS.gemini, promptData, './prediction_google.json', 'Google');

    console.log("\n🎉 Генерация завершена! Теперь вы можете запустить 'node validate.js' для оценки.");
}

runGeneration();