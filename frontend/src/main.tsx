import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx' // Certifique-se que o App está apontando para o arquivo certo

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)