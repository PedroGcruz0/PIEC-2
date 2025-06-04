document.getElementById("form-login").addEventListener("submit", async function (event) {
  event.preventDefault();

  const usuario = document.getElementById("usuario").value;
  const senha = document.getElementById("senha").value;

  try {
    const resposta = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, senha }),
    });

    if (resposta.ok) {
      window.location.href = "/ex1.html"; // Muda para a página correta após login
    } else {
      document.getElementById("mensagem-erro").textContent = "Usuário ou senha inválidos";
    }
  } catch (erro) {
    document.getElementById("mensagem-erro").textContent = "Erro ao conectar com o servidor";
  }
});

