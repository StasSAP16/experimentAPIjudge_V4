// correlate_tfi.js
const fs = require('fs');

function loadLatestMetrics(modelName) {
  const files = fs.readdirSync('.').filter(f => f.startsWith(`metrics_${modelName}`) && f.endsWith('.json'));
  if (files.length === 0) throw new Error(`❌ Не найдены метрики для ${modelName}. Сначала запустите validate.js`);
  const latest = files.sort().pop();
  return JSON.parse(fs.readFileSync(latest, 'utf8'));
}

function runCorrelation() {
  console.log('\n🔗 Запуск автоматической корреляции TFI и метрик валидации...');

  if (!fs.existsSync('./tokenizer_report.json')) {
    throw new Error('❌ tokenizer_report.json не найден. Сначала запустите analyze_tokenizers.js');
  }

  const tokReport = JSON.parse(fs.readFileSync('./tokenizer_report.json', 'utf8'));
  const dsMetrics = loadLatestMetrics('DeepSeek');
  const gemMetrics = loadLatestMetrics('Google');

  const phrases = Object.keys(tokReport.fragmentation_analysis);
  const models = { deepseek: dsMetrics, gemini: gemMetrics };

  // 1. Расчёт среднего TFI по модели
  const avgTFI = {};
  for (const m of ['deepseek', 'gemini']) {
    const tfis = phrases.map(p => tokReport.fragmentation_analysis[p][m].TFI);
    avgTFI[m] = tfis.reduce((a, b) => a + b, 0) / tfis.length;
  }

  // 2. Таблица пофразного сравнения
  console.log('\n📊 TFI vs Validation Metrics (Per-Phrase)');
  console.log('═'.repeat(95));
  console.log('Constraint Phrase          | DS_TFI | Gem_TFI | ΔTFI  | DS_NoMatch% | Gem_NoMatch% | ΔNoMatch');
  console.log('─'.repeat(95));

  for (const phrase of phrases) {
    const dsTFI = tokReport.fragmentation_analysis[phrase].deepseek.TFI;
    const gemTFI = tokReport.fragmentation_analysis[phrase].gemini.TFI;
    const deltaTFI = (gemTFI - dsTFI).toFixed(2);
    const dsNM = dsMetrics.metrics['No Match']?.percentage || dsMetrics.metrics['No  Match']?.percentage || 0;
    const gemNM = gemMetrics.metrics['No Match']?.percentage || gemMetrics.metrics['No  Match']?.percentage || 0;
    const deltaNM = (gemNM - dsNM).toFixed(2);
    console.log(`${phrase.padEnd(26)} | ${dsTFI.toFixed(2).padStart(6)} | ${gemTFI.toFixed(2).padStart(6)} | ${deltaTFI.padStart(5)} | ${dsNM.toFixed(2).padStart(11)}% | ${gemNM.toFixed(2).padStart(12)}% | ${deltaNM.padStart(8)}%`);
  }

  // 3. Агрегированное сравнение моделей
  console.log('\n📈 Aggregate Model Comparison');
  console.log('═'.repeat(75));
  console.log(`Model       | Avg TFI | No Match % | Granularity Diff % | Functional Eq % | Coverage %`);
  console.log('─'.repeat(75));
  for (const [key, name] of [['deepseek', 'DeepSeek'], ['gemini', 'Google']]) {
    const m = models[key];
    const nmKey = m.metrics['No Match'] || m.metrics['No  Match'] || { percentage: 0 };
    const gdKey = m.metrics['Granularity Difference'] || { percentage: 0 };
    const feKey = m.metrics['Functional Equivalence'] || { percentage: 0 };
    console.log(`${name.padEnd(11)} | ${avgTFI[key].toFixed(2).padStart(7)} | ${nmKey.percentage.toFixed(2).padStart(10)}% | ${gdKey.percentage.toFixed(2).padStart(18)}% | ${feKey.percentage.toFixed(2).padStart(15)}% | ${m.coverage.toFixed(2).padStart(8)}%`);
  }

  // 4. Направленная корреляция (Delta Analysis)
  console.log('\n🔍 Directional Correlation (ΔTFI vs ΔMetrics)');
  const deltaTFI_avg = avgTFI.gemini - avgTFI.deepseek;
  const dsNM = dsMetrics.metrics['No Match']?.percentage || dsMetrics.metrics['No  Match']?.percentage || 0;
  const gemNM = gemMetrics.metrics['No Match']?.percentage || gemMetrics.metrics['No  Match']?.percentage || 0;
  const deltaNM = gemNM - dsNM;
  const deltaGD = (gemMetrics.metrics['Granularity Difference']?.percentage || 0) - (dsMetrics.metrics['Granularity Difference']?.percentage || 0);
  const deltaFE = (gemMetrics.metrics['Functional Equivalence']?.percentage || 0) - (dsMetrics.metrics['Functional Equivalence']?.percentage || 0);

  const sign = (v) => v > 0 ? '↑' : v < 0 ? '↓' : '→';
  console.log(`Δ Avg TFI (Gem - DS): ${sign(deltaTFI_avg)} ${deltaTFI_avg.toFixed(2)}`);
  console.log(`Δ No Match %:         ${sign(deltaNM)} ${deltaNM.toFixed(2)}% ${deltaTFI_avg > 0 && deltaNM > 0 ? '✅ Positive correlation' : '⚠️ Inverse/Neutral'}`);
  console.log(`Δ Granularity Diff %: ${sign(deltaGD)} ${deltaGD.toFixed(2)}% ${deltaTFI_avg > 0 && deltaGD > 0 ? '✅ Positive correlation' : '⚠️ Inverse/Neutral'}`);
  console.log(`Δ Functional Eq %:    ${sign(deltaFE)} ${deltaFE.toFixed(2)}% ${deltaTFI_avg > 0 && deltaFE < 0 ? '✅ Negative correlation (expected)' : '⚠️ Direct/Neutral'}`);

  // 5. Сохранение отчёта
  const report = {
    timestamp: new Date().toISOString(),
    average_tfi: avgTFI,
    per_phrase_comparison: phrases.map(p => ({
      phrase: p,
      deepseek_tfi: tokReport.fragmentation_analysis[p].deepseek.TFI,
      gemini_tfi: tokReport.fragmentation_analysis[p].gemini.TFI,
      delta_tfi: parseFloat((tokReport.fragmentation_analysis[p].gemini.TFI - tokReport.fragmentation_analysis[p].deepseek.TFI).toFixed(3))
    })),
    model_metrics: { deepseek: dsMetrics.metrics, gemini: gemMetrics.metrics },
    delta_analysis: { 
      delta_tfi: parseFloat(deltaTFI_avg.toFixed(3)), 
      delta_no_match: parseFloat(deltaNM.toFixed(3)), 
      delta_granularity: parseFloat(deltaGD.toFixed(3)), 
      delta_functional: parseFloat(deltaFE.toFixed(3)) 
    }
  };
  fs.writeFileSync('./tfi_validation_correlation.json', JSON.stringify(report, null, 2));
  console.log('\n💾 Корреляционный отчёт сохранён в tfi_validation_correlation.json');
}

runCorrelation();