exports.login = (req, res) => {
  const { usuario, senha } = req.body;

  const usuarioValido = 'admin';
  const senhaValida = '123456';

  if (usuario === usuarioValido && senha === senhaValida) {
    return res.status(200).json({ mensagem: 'Login bem-sucedido' });
  }

  return res.status(401).json({ mensagem: 'Credenciais inválidas' });
};
