document.querySelectorAll('.role-choice').forEach(button=>button.addEventListener('click',()=>{document.querySelector('#username').value=button.dataset.user;document.querySelector('#password').value='DemoCare2026!';document.querySelectorAll('.role-choice').forEach(x=>x.classList.remove('selected'));button.classList.add('selected');}));
document.querySelectorAll('form').forEach(form=>form.addEventListener('submit',event=>{if(form.dataset.confirm&&!confirm(form.dataset.confirm)){event.preventDefault();return;}if(event.defaultPrevented)return;form.setAttribute('aria-busy','true');const button=event.submitter;if(button){button.classList.add('is-loading');setTimeout(()=>button.classList.remove('is-loading'),10000);}}));
document.querySelector('.mobile-menu')?.addEventListener('click',()=>document.body.classList.toggle('nav-open'));
document.addEventListener('keydown',event=>{if(event.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){const input=document.querySelector('.global-search input');if(input){event.preventDefault();input.focus();}}});
document.querySelector('.print-page')?.addEventListener('click',()=>window.print());
document.querySelector('.preview-note')?.addEventListener('click',()=>{const target=document.querySelector('#preview-content');target.replaceChildren();['subjective','objective','assessment','plan'].forEach(name=>{const title=document.createElement('h3');title.textContent=name[0].toUpperCase()+name.slice(1);const p=document.createElement('p');p.textContent=document.querySelector(`[name="${name}"]`).value;target.append(title,p);});document.querySelector('#note-dialog').showModal();});
document.querySelector('.close-dialog')?.addEventListener('click',()=>document.querySelector('#note-dialog').close());
document.querySelector('.apply-template')?.addEventListener('click',()=>{const prompts={subjective:'Chief complaint: [complete]\nHPI: [complete]\nReview of systems: [complete]',objective:'Vitals: [review]\nPhysical examination: [complete]\nRelevant results: [review]',assessment:'Assessment and working diagnoses: [complete]',plan:'Treatment: [complete]\nTests / referrals: [complete]\nFollow-up: [complete]\nPatient instructions: [complete]'};Object.entries(prompts).forEach(([name,value])=>{const field=document.querySelector(`[name="${name}"]`);if(!field.value.trim())field.value=value;});});

// Enhance the existing scoped native selects, retaining native keyboard behavior.
document.querySelectorAll('select[data-search-select]').forEach(select => {
  const options = Array.from(select.options).map(option => option.cloneNode(true));
  const input = document.createElement('input');
  input.type = 'search'; input.id = `${select.id}-search`;
  input.placeholder = select.dataset.searchSelect === 'patient' ? 'Type a name or MRN…' : 'Type a diagnosis or patient…';
  const label = document.createElement('label'); label.htmlFor = input.id;
  label.textContent = select.dataset.searchSelect === 'patient' ? 'Search patient by name or MRN' : 'Search diagnosis';
  const status = document.createElement('small'); status.id = `${select.id}-search-status`;
  status.setAttribute('role','status'); select.setAttribute('aria-describedby',status.id);
  select.before(label,input); select.after(status);
  const selectedSummary=document.createElement('div'); selectedSummary.className='selected-record';
  selectedSummary.setAttribute('role','status'); status.after(selectedSummary);
  const filter = () => {
    const selected = select.value;
    const words = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    const matches = options.filter(option => option.value && words.every(word => option.textContent.toLocaleLowerCase().includes(word)));
    const visible = options.filter(option => !option.value || option.value === selected || matches.includes(option));
    select.replaceChildren(...visible.map(option => option.cloneNode(true)));
    select.value = selected;
    selectedSummary.textContent = selected ? 'Selected: ' + select.selectedOptions[0].textContent : '';
    select.size = words.length ? Math.min(6,Math.max(2,visible.length)) : 1;
    status.textContent = words.length ? `${matches.length ? `${matches.length} matching choices.` : 'No matches.'} Current selection stays until you choose another.` : 'Type to narrow the list, then select a patient or record.';
  };
  input.addEventListener('input',filter);
  input.addEventListener('keydown',event => {
    if(event.key === 'Enter'){event.preventDefault();select.focus();}
    if(event.key === 'Escape'){input.value='';filter();}
  });
  select.addEventListener('change',()=> {input.value='';filter();});
  filter();
});

const height = document.querySelector('#id_height'), weight = document.querySelector('#id_weight');
const heightUnit = document.querySelector('#id_height_unit'), weightUnit = document.querySelector('#id_weight_unit');
const bmi = document.querySelector('#bmi-preview');
if(height && weight && heightUnit && weightUnit){
  const factor = unit => ({in:2.54,cm:1,lb:0.45359237,kg:1})[unit];
  const values = new Map();
  const preview = () => {
    const h=values.get(height), w=values.get(weight);
    if(bmi) bmi.textContent = h>0 && w>0 ? `BMI preview: ${(w / ((h/100)**2)).toFixed(1)}` : 'Enter height and weight to calculate BMI.';
  };
  [[height,heightUnit],[weight,weightUnit]].forEach(([field,unit]) => {
    const hidden=document.querySelector(`#id_${field.name}_canonical`);
    const supplied=Number(hidden?.value), displayed=Number(field.value);
    let canonical=field.value==='' ? null : displayed*factor(unit.value);
    if(hidden?.value && Number.isFinite(supplied) && Math.abs(supplied/factor(unit.value)-displayed)<=0.005)canonical=supplied;
    const sync=()=>{values.set(field,canonical);if(hidden)hidden.value=canonical===null?'':canonical.toFixed(8);preview();};
    field.addEventListener('input',()=>{canonical=field.value===''?null:Number(field.value)*factor(unit.value);sync();});
    field.addEventListener('blur',()=>{if(field.value!=='' && Number.isFinite(canonical)){field.value=String(Number((canonical/factor(unit.value)).toFixed(2)));sync();}});
    unit.addEventListener('change',()=>{
      if(canonical!==null && Number.isFinite(canonical))field.value=String(Number((canonical/factor(unit.value)).toFixed(2)));
      sync();
    });
    sync();
  });
}

document.querySelector('[data-schedule-filters]')?.addEventListener('change',event=>{
  if(event.target.matches('select,input[type=date]'))event.currentTarget.requestSubmit();
});
// A restored payment form returns to a fresh balance instead of replaying an old amount.
window.addEventListener('pageshow',event=>{
  const form=document.querySelector('[data-payment-return]');
  const restored=event.persisted || performance.getEntriesByType('navigation')[0]?.type==='back_forward';
  if(form && restored)window.location.replace(form.dataset.paymentReturn);
});

// Message badges stay current in visible pages; no external notification service.
if(document.querySelector('.message-notification')){
  let busy=false;
  let navigating=false;
  let lastRefresh=Date.now();
  let lastCount=Number(document.querySelector('.unread-count')?.textContent || 0);
  const refreshMessages=async()=>{
    if(busy || navigating || document.hidden || Date.now()-lastRefresh<5000)return;
    busy=true;
    lastRefresh=Date.now();
    try {
      const response=await fetch('/messages/notifications/',{headers:{Accept:'application/json'},cache:'no-store'});
      if(!response.ok || !response.headers.get('content-type')?.includes('application/json'))return;
      const data=await response.json();
      document.querySelectorAll('.unread-count').forEach(badge=>{badge.textContent=data.count;badge.hidden=!data.count;});
      document.querySelector('.message-notification').setAttribute('aria-label',`Messages, ${data.count} unread`);
      document.querySelectorAll('tr[data-thread-id]').forEach(row=>{
        const count=data.threads[row.dataset.threadId]||0;
        row.classList.toggle('unread-thread',count>0);
        const label=row.querySelector('.unread-label'); if(label)label.hidden=!count;
      });
      if(data.count>lastCount)document.querySelector('#message-announcement').textContent=`You have ${data.count} unread messages.`;
      lastCount=data.count;
    } catch(error) { /* Keep last known badges during a network interruption. */ }
    finally {busy=false;}
  };
  // The initial badges are already server rendered. Avoid a redundant request on navigation.
  setInterval(refreshMessages,20000);
  document.addEventListener('submit',event=>{if(!event.defaultPrevented)navigating=true;});
  document.addEventListener('visibilitychange',refreshMessages);window.addEventListener('focus',refreshMessages);
}
document.addEventListener('keydown',event=>{if(event.key==='Escape')document.querySelector('details.profile')?.removeAttribute('open');});
document.addEventListener('click',event=>{const profile=document.querySelector('details.profile');if(profile&&!profile.contains(event.target))profile.removeAttribute('open');});
