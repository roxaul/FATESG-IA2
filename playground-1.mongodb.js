// Conectar ao banco de dados "startup"
use('startup');

// Buscar todos os funcionários cujo campo 'setor' seja "TI"
db.getCollection('funcionarios').find({
  setor: 'TI'
});
