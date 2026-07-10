import axios from "axios";
import { useEffect } from "react";
import { useState } from "react";

function DatasetView() {

    const [errorMessage, setError] = useState("");
    const [datasets, setDatasets] = useState([]);
    const [selectedDataset, setDataset] = useState("");
    const [search, setSearchItem] = useState("");


    useEffect(() => {

        //ignore is written here cuz suppose if someone clicks away from the page once its mounted and then axios finally returns response after that
        // then stuff will be cooked right so ignore just acts like a flag to tell the stuff to ignore the response

        let ignore = false;
        async function fetchDatasets() {

            try {
                const session_id = sessionStorage.getItem("session_id")
                const res = await axios.get("http://127.0.0.1:8000/datasets", {
                    headers: {
                        'Authorization': 'Bearer ' + session_id,
                    }
                });

                if (!ignore) {
                    setDatasets(res.data);
                }
            }
            catch (err) {
                if (!ignore) {
                  if (err.response === undefined) {
                      setError("Something went wrong");
                  }
                  else {
                    setError(err.response.data.detail);
                  }
                
              }

            }

        }

        fetchDatasets();

        return () => {
            ignore = true; // if unloads
        }
    }, []);

    const filteredDatasets = datasets.filter((dataset) => dataset.name.toLowerCase().includes(search.toLowerCase()));

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
                <label className="text-white text-3xl mb-2" htmlFor="datasets">Choose a dataset : </label>

                <input type="text" className="border border-gray-400 bg-white px-3 rounded-full w-86.25 m-3" id="searchDataset" placeholder="Search Dataset"
                    onChange={(e) => setSearchItem(e.target.value)}
                />

                <select id="datasets"
                    className="text-black bg-white rounded-2xl p-1 w-86.25"
                    value = {selectedDataset}
                    onChange = {(e) => setDataset(e.target.value)}

                >
                    <option value="" disabled hidden>Choose a dataset...</option>

                    {filteredDatasets.map((dataset) =>

                        <option

                            key={dataset.id} value={dataset.name}>{dataset.name}</option>

                        )}



                </select>

                <div className="flex col gap-3 mt-3">

                <label className="text-white text-xl" htmlFor="selectedDataset">Selected Dataset : </label>

                <div className="text-white text-xl" id="selectedDataset">{selectedDataset}</div>

                </div>


                <button className="rounded-full px-6 py-2 bg-white text-black mt-2 hover:bg-gray-100 transition-colors">Submit</button>



            </main>
            



        </div>


    )

}

export default DatasetView;
