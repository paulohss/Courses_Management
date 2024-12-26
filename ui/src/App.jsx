
import React, { useState } from 'react'
import './App.css'
import UserModalForm from './components/UserModalForm'
import Navbar from './components/NavBar'
import UserTableList from './components/UserTableList'
import RolesTableList from './components/RolesTableList'
import CoursesTableList from './components/CoursesTableList'
import axios from 'axios' 

function App() {

  const [isOpen, setIsOpen] = useState(false);
  const [modalMode, setModalMode] = useState('add');
  const [searchTerm, setSearchTerm] = useState('');
  const [userData, setUserData] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [refreshTable, setRefreshTable] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState('users'); // State to manage selected menu option


  //--------------------------------------------------------------------------------
  //  Function to handle modal open:
  //--------------------------------------------------------------------------------
  const handleOpen = (mode, user) => {
    setUserData(user);
    setIsOpen(true);
    setModalMode(mode);
  }

  //--------------------------------------------------------------------------------
  // Function to handle form submission:
  //--------------------------------------------------------------------------------
  const handleSubmit = async (newUserData) => {
    if (modalMode === 'add') { // Add mode

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/users', newUserData);
        console.log('User added', response.data);
        setRefreshTable(true); // Trigger table refresh

      } catch (error) {
        console.error('Error adding user', error.response.data);        
        extractError(error);
      }

    } else { // Edit mode      

      try {
        console.log('Edit user', userData);
        const response = await axios.put(`http://127.0.0.1:5000/api/users/${userData.id}`, newUserData);
        console.log('User updated', response.data);
        setRefreshTable(true); // Trigger table refresh
      } catch (error) {
        extractError(error);
      }
    }
  }

  //--------------------------------------------------------------------------------
  // Extract the content of the <p> tag from the error response
  //--------------------------------------------------------------------------------
  function extractError(error) {
    const parser = new DOMParser()
    const doc = parser.parseFromString(error.response.data, 'text/html')
    const errorMsg = doc.querySelector('p').textContent
    setErrorMessage(errorMsg)
  }

  //--------------------------------------------------------------------------------
  // Function to handle menu change
  // -------------------------------------------------------------------------------
  const handleMenuChange = (menu) => {
      setSelectedMenu(menu);
  }

  return (
    <>
      {/* Navbar component */}
      <Navbar onOpen={() => handleOpen('add')} onSearch={setSearchTerm} onMenuChange={handleMenuChange} selectedMenu={selectedMenu} />
      
      {/* Divider */}
      <div className="divider divider-secondary">
        {selectedMenu === 'users' ? 'Users' : selectedMenu === 'roles' ? 'Roles' : 'Courses'}
      </div>
      
      {/* Error message */}
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

      {/* Users UI */}
      {selectedMenu === 'users' && (
        <>
          <UserTableList handleOpen={handleOpen} searchTerm={searchTerm} refreshTable={refreshTable} setRefreshTable={setRefreshTable} />
          <UserModalForm isOpen={isOpen} onSubmit={handleSubmit} onClose={() => setIsOpen(false)} mode={modalMode} userData={userData} />
        </>
      )}

      {/* Roles UI */}
      {selectedMenu === 'roles' && (
        <div>          
          <RolesTableList handleOpen={handleOpen} searchTerm={searchTerm} refreshTable={refreshTable} setRefreshTable={setRefreshTable} />
        </div>
      )}

      {/* Courses UI */}
      {selectedMenu === 'courses' && (
        <div>          
          <CoursesTableList handleOpen={handleOpen} searchTerm={searchTerm} refreshTable={refreshTable} setRefreshTable={setRefreshTable} />
        </div>
      )}
    </>
  )


}

export default App
