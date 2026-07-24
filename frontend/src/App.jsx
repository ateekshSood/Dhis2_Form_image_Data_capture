import LoginForm from './components/login_form';
import DatasetView from './components/datasets_view';
import FormUpload from './components/form_upload';
import Review from './components/review';
import { useState } from 'react';


function App() {

    const [view, setView] = useState("login");
    const [dataset, setDataset] = useState("");


    return (
    <>
    
            {view === "login" && <LoginForm onLoginSuccess={() => setView("datasets")} />}
            {view === "datasets" && <DatasetView onSelectSuccess={() => setView("form_upload")} onSetDataset = {(dataset)=>setDataset(dataset)} />}
            {view === "form_upload" && <FormUpload selectedDataset={dataset} onUploadSuccess={() => setView("review")} />}
            {view === "review" && <Review/>}
            

    </>

    
  )
}

export default App
