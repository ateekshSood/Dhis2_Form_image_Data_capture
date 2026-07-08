import LoginForm from './components/login_form';
import { useState } from 'react';

function App() {

    const [view, setView] = useState("login");


    return (
    <>
    
          {view === "login" && <LoginForm onLoginSuccess={() => setView("datasets")} />}
            

    </>

    
  )
}

export default App
