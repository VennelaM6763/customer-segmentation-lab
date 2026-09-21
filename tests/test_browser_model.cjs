const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const data=JSON.parse(fs.readFileSync(path.join(root,'reports/analysis.json'),'utf8'));
const M=require(path.join(root,'demo/model.js'));
if(data.project==='bike'){
  data.parity_cases.features.forEach((x,i)=>assert.ok(Math.abs(M.predict(data.model,x)-data.parity_cases.predictions[i])<1e-7));
  const x=M.calendarFeatures('2012-01-01',false,2,20.5,25,60,6.7);
  assert.equal(x[0],1);assert.equal(x[6],0);assert.equal(x[7],1);assert.equal(x[9],.5);
  console.log('Browser inference matches all '+data.parity_cases.features.length+' Python test predictions.');
}else if(data.project==='segments'){
  data.points.forEach(p=>assert.equal(M.segment(data,data.selected_k,[p.recency,p.frequency,p.monetary]),p.cluster));
  console.log('Browser assignments match all '+data.points.length+' Python sample labels.');
}else{
  const vm=require('node:vm'),context={window:{}};
  vm.runInNewContext(fs.readFileSync(path.join(root,'demo/data.js'),'utf8'),context);
  assert.equal(JSON.stringify(context.window.PROJECT_DATA),JSON.stringify(data));
  console.log('Dashboard data matches the Python analysis export.');
}
