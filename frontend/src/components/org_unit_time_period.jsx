import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";

function OrgUnitTimePeriod({
    data_set_name,
    onSetDataSetId,
    onSetorgUnitId,
    onOTSelectSuccess,
    onSetTimePeriod,
}) {
    const [orgUnits, setOrgUnits] = useState([]);
    const [errorMessage, setError] = useState("");
    const [selectedOrgUnit, setSelectedOrgUnit] = useState("");
    const [search, setSearchItem] = useState("");

    useEffect(() => {
        async function getDetails() {
            try {
                const session_id = sessionStorage.getItem("session_id");
                const res = await axios.get(
                    `http://127.0.0.1:8000/dataset_org_units/${data_set_name}`,
                    {
                        headers: {
                            Authorization: "Bearer " + session_id,
                        },
                    },
                );
                setOrgUnits(res.data.orgUnit);
                onSetDataSetId(res.data.dataSetId);
            } catch (err) {
                if (err.response === undefined) {
                    setError("Something went wrong");
                } else {
                    setError(err.response.data.detail);
                }
            }
        }

        getDetails();
    }, []);

    const filteredOrgUnit = orgUnits.filter((orgUnit) =>
        orgUnit.name.toLowerCase().includes(search.toLowerCase()),
    );

    const handleSubmit = (e) => {
        e.preventDefault();
        onSetorgUnitId(selectedOrgUnit);
        onOTSelectSuccess();
    };

    return (
        <div className="min-h-screen flex flex-col bg-[#1d5288]">
            <header className="flex justify-end items-center  h-auto p-4">
                <div>
                    <a
                        href="https://github.com/ateekshSood/Dhis2_Form_image_Data_capture.git"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block opacity-100 transition-opacity duration-200 hover:opacity-70"
                    >
                        <img
                            src="GitHub_Invertocat_Black.svg"
                            alt="Github"
                            className="h-8 w-8"
                        ></img>
                    </a>
                </div>
            </header>

            <main className="flex-1 flex flex-col justify-center items-center gap-3">
                {errorMessage && (
                    <div className="text-red-500 font-bold">{errorMessage}</div>
                )}
                <label className="text-white text-3xl mb-2" htmlFor="datasets">
                    Choose a dataset :{" "}
                </label>

                <form
                    onSubmit={handleSubmit}
                    className="flex flex-col items-center w-full"
                >
                    <input
                        type="text"
                        className="border border-gray-400 bg-white px-3 rounded-full w-86.25 m-3"
                        id="searchDataset"
                        placeholder="Search OrgUnit"
                        onChange={(e) => setSearchItem(e.target.value)}
                    />

                    <select
                        id="OrgUnits"
                        className="text-black bg-white rounded-2xl p-1 w-86.25"
                        value={selectedOrgUnit}
                        onChange={(e) => setSelectedOrgUnit(e.target.value)}
                        required
                    >
                        <option value="" disabled hidden>
                            Choose an Org Unit...
                        </option>

                        {filteredOrgUnit.map((orgUnits) => (
                            <option key={orgUnits.id} value={orgUnits.id}>
                                {orgUnits.name}
                            </option>
                        ))}
                    </select>

                    <input
                        type="text"
                        className="border border-gray-400 bg-white px-3 rounded-full w-86.25 m-3"
                        placeholder="Enter Time Period"
                        required
                        onChange={(e) => onSetTimePeriod(e.target.value)}
                    />

                    <div className="flex col gap-3 mt-3">
                        <label
                            className="text-white text-xl"
                            htmlFor="selectedDataset"
                        >
                            Selected OrgUnit :{" "}
                        </label>
                    </div>

                    <button
                        type="submit"
                        className="rounded-full px-6 py-2 bg-white text-black mt-2 hover:bg-gray-100 transition-colors"
                    >
                        Submit
                    </button>
                </form>
            </main>
        </div>
    );
}

export default OrgUnitTimePeriod;
