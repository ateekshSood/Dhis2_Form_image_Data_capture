import { useState } from "react";
import axios from "axios";

function FormUpload({selectedDataset}) {

    const [file, setFile] = useState(null);
    const [errorMessage, setError] = useState("");
    
    async function fileUpload() {

        if (file === null) {
            setError("Please upload a file");
            
        }
        else {
          
          const formData = new FormData();
            formData.append("file", file);
            formData.append("dataset" , selectedDataset)
  
          try {
              const session_id = sessionStorage.getItem("session_id");
              const res = await axios.post("http://127.0.0.1:8000/upload", formData, {
                  headers: {
                      'Authorization': 'Bearer ' + session_id,
                  }
              });
              sessionStorage.setItem("upload_id", res.data)
              setError("");
          }
          catch (err) {
              if (err.response === undefined) {
                  setError("Something went wrong");
              }
              else {
                  setError(err.response.data.detail);
              }
          }
          
        }
       
  }


    
    return (
        <div className="min-h-screen flex flex-col bg-[#1d5288]">

          <header className="flex justify-end items-center  h-auto p-4">

              <div>

                  <a href="https://github.com/ateekshSood/Dhis2_Form_image_Data_capture.git" target="_blank" rel="noopener noreferrer"
                      className="inline-block opacity-100 transition-opacity duration-200 hover:opacity-70">
                      <img src="GitHub_Invertocat_Black.svg" alt="Github"
                        className="h-8 w-8"></img>
                  </a>

              </div>

            </header>

            <main className="flex-1 flex flex-col justify-center items-center gap-3">
                 {errorMessage && <div className="text-red-500 font-bold">{errorMessage}</div>}

                <label className="text-white text-3xl mb-2" htmlFor="file_upload">Select your form : </label>
                <input id="file_upload" type="file" placeholder="Choose Your File"
                    onChange={(e) => setFile(e.target.files[0])} 
                    className="text-sm text-white
                            file:mr-4 file:py-2 file:px-4
                            file:rounded-full file:border-0
                            file:text-sm file:font-semibold
                            file:bg-violet-50 file:text-black"
                    capture="environment"
                />

                <button className="rounded-full px-6 py-2 bg-white text-black mt-2 hover:bg-gray-100 transition-colors"
                    type="submit"
                    onClick={fileUpload}
                >Submit</button>


            </main>

          

        </div>
    )
}

export default FormUpload;