import { useState } from 'react'

function App() {

  return (
    <div className="min-h-screen flex flex-col">
          <header className="flex justify-end items-center border-4 border-solid border-red-600 h-auto p-4">

              <div>

                  <a href=""
                  
              </div>
              
          </header>

          

          <main className="flex-1 flex flex-col justify-center items-center gap-3  ">

            <div className="font-bold text-6xl font-mono w-min text-center border p-2 mb-18 mt-7  border-red-600">Dhis2 OCR Form Submission</div>
              

            <form
                className="flex flex-col justify-center  border-2 border-solid border-purple-500 rounded-2xl p-4 gap-3 max-w-md">
  
                  
                    <label htmlfor="username">Enter the Username : </label>
                    <input type="text" className="border border-gray-400 bg-white px-3" id="username" required />
    
                    <label htmlfor="password">Enter the Password : </label>
                    <input type="text" className="border border-gray-400 bg-white px-3" id="password" required/>
    
                
    
                  <button className=" border-4 solid border-blue-700 rounded-full w-full p-3">Submit</button>
  
            </form> 



          </main>


            
    </div>
  )
}

export default App
