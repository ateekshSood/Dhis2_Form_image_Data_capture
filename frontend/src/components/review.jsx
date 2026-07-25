import { useState , useEffect } from "react";
import axios from "axios";

function Review() {

    const [fields, setFields] = useState([]);
    const [loading, setLoading] = useState(true);
    const [errorMessage, setError] = useState("");
    const [overrides, setOverRides] = useState({});

    useEffect(() => {
        async function fetchMapping() {
            const upload_id = sessionStorage.getItem("upload_id");
            const session_id = sessionStorage.getItem("session_id");

            try {
                const res = await axios.post(`http://127.0.0.1:8000/field_mapping/${upload_id}`, null, {
                    headers: {
                        "Authorization": "Bearer " + session_id
                    }
                    
                });

                setFields(res.data);
                
            }
            catch (error) {
                if (error.response === undefined) {
                    setError("Something went wrong");
                }
                else {
                    setError(error.response.data.detail);
                }
            }
            finally {
                setLoading(false);
            }
            
        }
        fetchMapping();
    }, []);

    if (loading) {
        return (
            <div className="flex min-h-screen flex-col justify-center items-center bg-[#1d5288]">
              <div className="animate-spin h-12 w-12 border-4 border-white border-t-transparent rounded-full"></div>
            </div>            
        )
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

                <div className="bg-white rounded-2xl p-6 max-w-5xl w-full mx-4 overflow-x-auto">

                  <table className="w-full text-left border-collapse">
  
                      <thead>
                          <tr className="border-b-2 border-gray-300">
                            <th className="p-3 text-gray-700">Field Name</th>
                            <th className="p-3 text-gray-700">LLM Predicted Value</th>
                            <th className="p-3 text-gray-700">LLM Confidence Score</th>
                            <th className="p-3 text-gray-700">User Review Input (LEAVE EMPTY IF LLM OUTPUT IS CORRECT)</th>
                          </tr>
                      </thead>

                      <tbody>
                            
                        {fields.map((field) => (
    
                            <tr key={field.dataElementId} className="border-b border-gray-200 hover:bg-gray-50">
    
                                <td className="p-3 text-black font-medium">{field.name}</td>
                                <td className="p-3 text-black">{field.value}</td>
                                <td className={`p-3 ${field.confidence === "low" ? "bg-yellow-300 font-semibold" : "text-black"}`}>
                                            {field.confidence}
                                </td>
                                <td className="p-3">
                                  <input
                                    type="text"
                                    value={overrides[field.dataElementId] || ""}    
                                    className="border border-gray-400 bg-white px-3 py-1 rounded-full text-black w-full"
                                        onChange={(e) => setOverRides({...overrides  , [field.dataElementId] : e.target.value}) 
                                    }    
                                  />
                                </td>
                              
                            </tr>
                            
                        ))}


                      </tbody>
                      
                      
                    </table>
                </div>
                
            </main>
          
        </div>
    )
}

export default Review;