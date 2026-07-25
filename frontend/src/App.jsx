import LoginForm from './components/login_form';
import DatasetView from './components/datasets_view';
import FormUpload from './components/form_upload';
import Review from './components/review';
import OrgunitTimePeriod from './components/org_unit_time_period';
import { useState } from 'react';


function App() {

    const [view, setView] = useState("login");
    const [dataset, setDataset] = useState("");
    const [datasetId, setDatasetId] = useState("");
    const [orgUnitId, setOrgUnitId] = useState("");
    const [timePeriod, setTimePeriod] = useState("");


    return (
    <>
    
            {view === "login" && <LoginForm onLoginSuccess={() => setView("datasets")} />}
            {view === "datasets" && <DatasetView onSelectSuccess={() => setView("orgUnitAndTimePeriod")} onSetDataset={(dataset) => setDataset(dataset)} />}
            {view === "orgUnitAndTimePeriod" && <OrgunitTimePeriod
                data_set_name={dataset}
                onOTSelectSuccess={() => setView("form_upload")}
                onSetDataSetId={(dataset_id) => setDatasetId(dataset_id)}
                onSetorgUnitId={(org_unit_id) => setOrgUnitId(org_unit_id)}
                onSetTimePeriod={(time_period) => setTimePeriod(time_period)}
            />}
            {view === "form_upload" && <FormUpload
                selectedDataset={dataset}
                onUploadSuccess={() => setView("review")}
                org_unit_id={orgUnitId}
                time_period={timePeriod}
                dataset_id = {datasetId}
            />}
            {view === "review" && <Review/>}
            

    </>

    
  )
}

export default App
