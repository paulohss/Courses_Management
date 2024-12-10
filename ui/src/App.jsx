
import React, { useState } from 'react'
import './App.css'
import ModalForm from './components/ModalForm'
import Navbar from './components/NavBar'
import Tablelist from './components/Tablelist'
import axios from 'axios'
 
function App() {

  const [isOpen, setIsOpen] = useState(false);
  const [modalMode, setModalMode] = useState('add');
  const [searchTerm, setSearchTerm] = useState('');
  const [userData, setUserData] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleOpen = (mode) => {
    setIsOpen(true);
    setModalMode(mode);
  }

  const handleSubmit = async (newUserData) => {
    if (modalMode === 'add') {

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/users', newUserData );
        console.log('User added', response.data);
        
      } catch (error) {
        console.error('Error adding user', error.response.data);
        // Extract the content of the <p> tag from the error response
        const parser = new DOMParser();
        const doc = parser.parseFromString(error.response.data, 'text/html');
        const errorMsg = doc.querySelector('p').textContent;
        setErrorMessage(errorMsg);
      }

      
    } else {
      console.log('edit')
    }
  }

  return (
    <>
      <Navbar onOpen={() => handleOpen('add')} onSearch={setSearchTerm} />
      {errorMessage && (
        <div role="alert" className="alert alert-error">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 shrink-0 stroke-current"
            onClick={() => setErrorMessage('')}
            fill="none"
            viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Error! {errorMessage}</span>
        </div>
      )}          
      <Tablelist handleOpen={handleOpen} searchTerm={searchTerm} />    
      <ModalForm
        isOpen={isOpen} 
        onSubmit={handleSubmit} 
        onClose={() => setIsOpen(false)} 
        mode={modalMode}
        userData={userData}/>
    </>
  )
}

export default App
