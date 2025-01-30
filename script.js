// Incorrectly using 'var' instead of 'let' or 'const'
var clickMeBtn = document.getElementById('clickMeBtn');

clickMeBtn.addEventListener('click', function() {
    // Missing semicolon and bad string concatenation
    alert('Button was clicked ' + 'k' )

    // Global variable leak, which is bad practice
    someGlobalVariabl..  = 'This is a global variable';
});
