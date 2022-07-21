// Script entier en mode strict
"use strict";

const upload_btn = document.getElementById('btn_upload')
const oct_image = !!document.getElementById('oct_image')

const diagnose_btn = document.getElementById('btn_diagnose')
const oct_image_diagnose = !!document.getElementById('oct_image_diagnose')
let col_right = document.getElementById('diagnose')

document.addEventListener('DOMContentLoaded', () => {

	if(oct_image){
		browser.classList.add('hidden');
		upload_btn.innerHTML='Change OCT image'
	}
	if(oct_image_diagnose){
		diagnose_btn.classList.add('hidden');
		col_right.classList.remove('regular-grid');
	}

});
