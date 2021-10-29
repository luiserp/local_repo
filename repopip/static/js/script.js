var acept_button = document.querySelector('button#Apply')
var cancel_button = document.querySelector('button#Cancel')
var form = document.querySelector('#conf-form');
var configs_div = document.querySelector('#configs');
var blocks = document.querySelectorAll('.block');
var configs = document.querySelectorAll('.edit-config .select');
var backdrop = document.querySelector('.backdrop');
var prop = document.querySelector('.prop');

let selected_block;
let selected_config;

document.addEventListener('DOMContentLoaded', function() {
    loadConfigs();
});

for (let i = 0; i < blocks.length; i++) {
    blocks[i].addEventListener('click', function(){
        blocks.forEach(b=>{b.classList.remove('active')});
        blocks[i].classList.add('active');
        selected_block = blocks[i].id;
    });    
}

for (let i = 0; i < configs.length; i++) {
    configs[i].addEventListener('click', function(){
        configs.forEach(b=>{b.classList.remove('active')});
        configs[i].classList.add('active');
        selected_config = configs[i].id;
        if(selected_config == 'personalised'){
            configs[i].classList.add('expand')
        }else{
            form.parentElement.classList.remove('expand')
        }
    });    
}

acept_button.addEventListener('click', async function(){
    let error = [];
    if( selected_block == null ){
        error.push(`Debe seleccionar un nivel`)
    }
    if ( selected_config == null ) {
        error.push(`Debe seleccionar una configuraci&oacute;n`)
    }
    if(error != '') {
        showMessage({ title: 'Seleccione los parametros', message:error }, false);
        return
    }
    data = {
        'level': selected_block,
    }
    data['config'] = selected_config == 'standar' ? selected_config : form['conf'].value;
    let { result } = await SetConfig(data)
    if(result) {
        showMessage({ title:'Configuraci&oacute;n aplicada', message: [`La configuraci&oacute;n a nivel '${selected_block}' se aplic&oacute; correctamente`] });
        await loadConfigs();
        resetButtonStatus();
    }else{
        showMessage({ title:'Ha ocurrido un error', message: [`No se ha podido establecer la configuraci&oacute;n`] }, false);
    }
});

cancel_button.addEventListener('click', function() {
    resetButtonStatus();
})

backdrop.addEventListener('click', function() {
    prop.classList.remove('open')
    backdrop.classList.remove('open')
    setTimeout(() => {
        prop.style.display = 'none'
        backdrop.style.display = 'none'
    }, 400);
});

async function loadConfigs (){
    resp = await getConfigs();
    if(resp['error']){
        return
    }
    if(resp['configs'].length != 0){
        configs_div.style.display = 'block'
        var ul = configs_div.querySelector('ul');
        ul.innerHTML = ''
        for( c of resp['configs']){
            let li = document.createElement('li')
            li.innerHTML = `<strong>${c[0]}</strong>: ${c[1]}`
            ul.appendChild(li)
        }
    }else{
        configs_div.style.display = 'none'
    }
}

function showMessage( {title, message}, success = true ){
    prop.querySelector('.prop-message').innerHTML = '';
    if(!success){
        prop.querySelector('.prop-title h3').style.color = 'red';
    }else{
        prop.querySelector('.prop-title h3').style.color = '#5f686d';
    }
    prop.querySelector('.prop-title h3').innerHTML = title;
    for( m of message ){
        p = document.createElement('p')
        p.innerHTML = m
        prop.querySelector('.prop-message').appendChild(p);
    }
    // Para cargar la animacion hay q cambiar el display y un instante despues añadir la clase.
    prop.style.display = 'block'
    backdrop.style.display = 'block'
    setTimeout(() => {
        prop.classList.add('open')
        backdrop.classList.add('open')
    }, 10);
}

async function SetConfig(data){
    const resp = await fetch('/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    return resp.json();
}

async function getConfigs(){
    const resp = await fetch('/get-configs');
    return resp.json();
}

function resetButtonStatus() {
    for (let i = 0; i < blocks.length; i++) {
        blocks[i].classList.remove('active');
    }
    for (let i = 0; i < configs.length; i++) {
        configs[i].classList.remove('active');
    }
    form.parentElement.classList.remove('expand');

    selected_block = null
    selected_config = null
}