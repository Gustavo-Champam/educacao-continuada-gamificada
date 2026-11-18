const {chromium}=require('../frontend/node_modules/@playwright/test');
const fs=require('fs');
const config={AF_ADMIN_PASSWORD:process.env.AF_ADMIN_PASSWORD||'af-demo-champam-2026'};
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1100}});
  page.setDefaultTimeout(20000);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8085/af.html');
  await page.locator('#password').fill(config.AF_ADMIN_PASSWORD);
  await page.getByRole('button',{name:'Consultar alunos',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#students').textContent.includes('Ana AF'));
  await page.getByRole('button',{name:'Consultar catÃ¡logo',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#catalog').textContent.includes('JAVA-01'));
  await page.getByRole('button',{name:'Classificar perfil',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#prediction').textContent.includes('probabilities'));
  await page.getByRole('button',{name:'Executar agente',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('403'));
  await page.locator('#password').fill('');
  await page.screenshot({path:'evidencias/af-ci/interface.png',fullPage:true});
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync('evidencias/af-ci/interface.json',JSON.stringify({status:'passed',checks:['consulta alunos','catalogo','classificacao real','agente sem consentimento: 403','sem erros JavaScript']},null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
