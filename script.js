function login() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const message = document.getElementById('message');
  
    if (user === 'admin' && pass === '1234') {
      message.style.color = 'green';
      message.textContent = 'Login bem-sucedido!';
    } else {
      message.style.color = 'red';
      message.textContent = 'Usuário ou senha incorretos.';
    }
  }
  