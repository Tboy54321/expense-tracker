// ALL SCRIPTS RELATED TO PASSWORD AND VERIFICATIONS
const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
    console.log('Switch mode changed');
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})
