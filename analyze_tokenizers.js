// analyze_tokenizers.js
const fs = require('fs');

// 🔑 ВСТАВЬТЕ ВАШ ДЕЙСТВИТЕЛЬНЫЙ КЛЮЧ GEMINI API
const GEMINI_API_KEY = 'xxx';
const GEMINI_COUNT_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:countTokens';

const CONSTRAINT_PHRASES = [
  'MUST EXACTLY MATCH',
  'decomposition_result',
  'Do NOT describe',
  'observable staff actions',
  'HIS',
  'scanner',
  'printer',
  'filing cabinet'
];

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function countGeminiTokens(text) {
  const res = await fetch(`${GEMINI_COUNT_URL}?key=${GEMINI_API_KEY}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text }] }] })
  });
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Gemini countTokens API Error ${res.status}: ${errText}`);
  }
  const data = await res.json();
  return data.totalTokens;
}

async function inferGeminiBoundaries(text) {
  const boundaries = [];
  let prev = 0;
  const total = text.length;
  console.log(`📏 Начало посимвольного сканирования Gemini (${total} символов). Это займёт ~1-2 мин...`);
  
  for (let i = 1; i <= total; i++) {
    const curr = await countGeminiTokens(text.slice(0, i));
    if (curr > prev) {
      boundaries.push(i);
      prev = curr;
    }
    if (i % 300 === 0) {
      console.log(`   ... обработано ${i}/${total} символов`);
      await sleep(50);
    }
  }
  return boundaries;
}

function computeTFI(tokens, phrase) {
  const words = phrase.trim().split(/\s+/).length;
  return tokens.length / words;
}

async function runAnalysis() {
  console.log('🔍 Загрузка prompt.json...');
  if (!fs.existsSync('./prompt.json')) {
    throw new Error('❌ Файл prompt.json не найден в текущей директории.');
  }
  const prompt = JSON.parse(fs.readFileSync('./prompt.json', 'utf8'));
  const promptText = JSON.stringify(prompt, null, 2);

  try {
    console.log('⏳ Загрузка токенизатора DeepSeek...');
    const { AutoTokenizer } = await import('@huggingface/transformers');
    
    const dsTokenizer = await AutoTokenizer.from_pretrained('deepseek-ai/deepseek-llm-7b-base', {
      progress_callback: false,
      local_files_only: false
    });

    const rawIds = dsTokenizer.encode(promptText);
    const dsIds = Array.isArray(rawIds) ? rawIds : rawIds.input_ids;

    let dsTokens;
    if (typeof dsTokenizer.convert_ids_to_tokens === 'function') {
      dsTokens = dsTokenizer.convert_ids_to_tokens(dsIds);
    } else if (dsTokenizer.model && typeof dsTokenizer.model.convert_ids_to_tokens === 'function') {
      dsTokens = dsTokenizer.model.convert_ids_to_tokens(dsIds);
    } else {
      dsTokens = dsIds.map(id => dsTokenizer.decode([id], { skip_special_tokens: false }).replace(/^Ġ|^ /, ''));
    }
    console.log(`✅ DeepSeek: ${dsIds.length} токенов загружено.`);

    console.log('⏳ Восстановление границ токенов Gemini...');
    const gemBounds = await inferGeminiBoundaries(promptText);
    const gemTokens = gemBounds.map((end, i) => {
      const start = i === 0 ? 0 : gemBounds[i - 1];
      return promptText.slice(start, end);
    });
    console.log(`✅ Gemini: ${gemBounds.length} границ восстановлено.`);

    const report = { 
      prompt_length_chars: promptText.length,
      deepseek: { total_tokens: dsIds.length, tokens: dsTokens },
      gemini: { total_tokens: gemBounds.length, tokens: gemTokens, method: 'perturbation_boundary_testing' },
      fragmentation_analysis: {}
    };

    for (const phrase of CONSTRAINT_PHRASES) {
      const phraseLower = phrase.toLowerCase();
      
      const dsMatches = dsTokens.filter(t => {
        const cleanT = t.replace('Ġ', ' ').replace('Ċ', '\n').toLowerCase();
        return cleanT.includes(phraseLower) || phraseLower.includes(cleanT);
      });
      
      const gemMatches = gemTokens.filter(t => {
        const cleanT = t.toLowerCase();
        return cleanT.includes(phraseLower) || phraseLower.includes(cleanT);
      });

      report.fragmentation_analysis[phrase] = {
        deepseek: { tokens: dsMatches.length, TFI: computeTFI(dsMatches, phrase) },
        gemini: { tokens: gemMatches.length, TFI: computeTFI(gemMatches, phrase) },
        bias_direction: dsMatches.length > gemMatches.length ? 'DeepSeek_fragments_more' : 'Gemini_fragments_more'
      };
    }

    const jsonChars = ['{', '}', '[', ']', '"', ':', ','];
    const dsJsonRatio = dsTokens.filter(t => jsonChars.includes(t.trim())).length / dsIds.length;
    const gemJsonRatio = gemTokens.filter(t => jsonChars.includes(t.trim())).length / gemBounds.length;
    report.json_syntax_ratio = { deepseek: dsJsonRatio, gemini: gemJsonRatio };

    fs.writeFileSync('./tokenizer_report.json', JSON.stringify(report, null, 2));
    console.log('\n✅ tokenizer_report.json успешно сохранён.');
    console.log('📊 Полный порядок следующих шагов:');
    console.log('   1️⃣ node generate.js      → создание prediction_*.json');
    console.log('   2️⃣ node validate.js      → оценка качества и экспорт metrics_*.json');
    console.log('   3️⃣ node correlate_tfi.js → корреляция TFI и метрик валидации');
    
  } catch (error) {
    console.error('\n❌ Критическая ошибка при анализе токенизаторов:');
    console.error(error.message);
    process.exit(1);
  }
}

runAnalysis();