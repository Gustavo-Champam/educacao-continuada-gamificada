const {chromium}=require('../frontend/node_modules/@playwright/test');
const fs=require('fs');
const config={AF_ADMIN_PASSWORD:process.env.AF_ADMIN_PASSWORD||'af-demo-champam-2026'};
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.AF_BROWSER_CHANNEL?{channel:process.env.AF_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1100}});
  page.setDefaultTimeout(20000);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8085/af.html');
  await page.locator('#password').fill(config.AF_ADMIN_PASSWORD);
  await page.getByRole('button',{name:'Consultar alunos',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#students').textContent.includes('Ana AF'));
  await page.getByRole('button',{name:'Consultar catálogo',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#catalog').textContent.includes('JAVA-01'));
  await page.getByRole('button',{name:'Classificar perfil',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#prediction').textContent.includes('probabilities'));
  await page.getByRole('button',{name:'Executar agente',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('403'));
  // Regressão de privacidade: resposta antiga não reaparece após trocar aluno.
  // Esta parte simula apenas a demora HTTP; a geração real é testada no script Python.
  let liberar, recebido;
  const espera=new Promise(resolve=>{liberar=resolve});
  const iniciou=new Promise(resolve=>{recebido=resolve});
  await page.route('**/api/af/alunos/1/agente',async route=>{
    recebido();await espera;
    await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({resposta:'RESPOSTA_ANTIGA',geracao:true,fontes:[]})});
  });
  await page.locator('#consent').check();
  await page.getByRole('button',{name:'Executar agente',exact:true}).click();
  await iniciou;
  await page.locator('#student').fill('2');
  if(await page.locator('#consent').isChecked())throw Error('Consentimento reaproveitado para outro aluno');
  liberar();
  await page.waitForFunction(()=>!document.querySelector('button').disabled);
  if((await page.locator('#recommendation').textContent()).includes('RESPOSTA_ANTIGA'))throw Error('Resposta exibida em contexto diferente');
  await page.unroute('**/api/af/alunos/1/agente');
  await page.locator('#password').fill('');
  await page.screenshot({path:'evidencias/af-ci/interface.png',fullPage:true});
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync('evidencias/af-ci/interface.json',JSON.stringify({status:'passed',checks:['consulta alunos','catalogo','classificacao real','agente sem consentimento: 403','troca de aluno revoga consentimento','resposta tardia descartada (HTTP simulado)','sem erros JavaScript']},null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
