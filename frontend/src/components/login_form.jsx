import axios from 'axios';
import { useState } from 'react';


function LoginForm() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setError] = useState("");
    
    async function handleSubmit(e) {

        e.preventDefault();
        
  
        try {
            
          const res = await axios.post("http://127.0.0.1:8000/Credentials/", {
              username: username,
              password: password
          });
          setError("");
          sessionStorage.setItem("session_id", res.data)
      }
      catch (error) {
            setError(error.response.data);
        }

        setUsername("");
        setPassword("");
      
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

          

          <main className="flex-1 flex flex-col justify-center items-center gap-3  ">

              <div className="font-bold text-6xl font-mono w-min text-center p-2 mb-18 mt-7 text-white ">Dhis2 OCR Form Submission</div>

              {errorMessage && <div className="text-red-500 font-bold">{errorMessage}</div>}
              

            <form
                  className="flex flex-col  rounded-2xl p-4 gap-3 max-w-md"
                  onSubmit={handleSubmit}>
                    
                  <label htmlFor="username" className="text-white">Enter the Username : </label>
                  <input type="text" className="border border-gray-400 bg-white px-3 rounded-full" id="username" placeholder="username" value={username} required
                  onChange={(e) => setUsername(e.target.value)}/>
    
                  <label htmlFor="password" className="text-white">Enter the Password : </label>
                  <input type="password" className="border border-gray-400 bg-white px-3 rounded-full" id="password" placeholder="password" value={password} required
                  onChange={(e) => setPassword(e.target.value)}
                  />
    
                
    
                  <button className="rounded-full w-full p-2 bg-white text-black mt-2">Submit</button>
  
            </form> 



          </main>


            
    </div>
  )
}

export default LoginForm;
