import LoginForm from './components/login_form';
import DatasetView from './components/datasets_view';
import { useState } from 'react';

function App() {

    const [view, setView] = useState("login");


    return (
    <>
    
            {view === "login" && <LoginForm onLoginSuccess={() => setView("datasets")} />}
            {view === "datasets" && <DatasetView/>}
            

    </>

    
  )
}

export default App
