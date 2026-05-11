function App() {
  return (
    <div style={{ fontFamily: 'sans-serif', padding: '20px' }}>
      <h1>🚗 Locadora Guilherme</h1>
      <p>A Certeza do Melhor!!</p>
      
      <section style={{ marginTop: '40px', border: '1px solid #ccc', padding: '20px' }}>
        <h2>Cadastro de Veículo</h2>
        <input type="text" placeholder="Modelo do carro" />
        <input type="text" placeholder="Placa" />
        <button onClick={() => alert('Em breve integraremos com o Python!')}>
          Cadastrar
        </button>
      </section>
    </div>
  )
}

export default App