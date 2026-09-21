
/* Portable inference. This file is also tested against Python-generated cases. */
(function(root){
function predict(model,features){if(model.type==='constant')return model.value;if(model.type==='linear')return model.intercept+model.coef.reduce((s,c,i)=>s+c*features[i],0);const values=features.map(Math.fround);return model.trees.reduce((sum,t)=>{let n=0;while(t.left[n]!==-1)n=values[t.feature[n]]<=t.threshold[n]?t.left[n]:t.right[n];return sum+t.value[n]},0)/model.trees.length}
function segment(data,k,values){const z=values.map((v,i)=>(Math.log1p(v)-data.mean[i])/data.scale[i]);let best=0,distance=Infinity;data.models[String(k)].centers.forEach((c,i)=>{const d=c.reduce((s,v,j)=>s+(v-z[j])**2,0);if(d<distance){distance=d;best=i}});return best}
function calendarFeatures(date,holiday,weather,temp,feel,humidity,wind){const d=new Date(date+'T12:00:00Z'),month=d.getUTCMonth()+1,day=d.getUTCDay();return [d.getUTCFullYear()-2011,Math.sin(2*Math.PI*month/12),Math.cos(2*Math.PI*month/12),Math.sin(2*Math.PI*day/7),Math.cos(2*Math.PI*day/7),holiday?1:0,!holiday&&day>0&&day<6?1:0,weather===2?1:0,weather===3?1:0,temp/41,feel/50,humidity/100,wind/67]}
root.ProjectModel={predict,segment,calendarFeatures};if(typeof module!=='undefined')module.exports=root.ProjectModel;
})(typeof window!=='undefined'?window:globalThis);
