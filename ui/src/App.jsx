
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

  const handleOpen = (mode) => {
    setIsOpen(true);
    setModalMode(mode);
  }

  const handleSubmit = () => {
    if (modalMode === 'add') {
      console.log('add')
    } else {
      console.log('edit')
    }
  }

  return (
    <>
      <Navbar onOpen={() => handleOpen('add')} onSearch={setSearchTerm} />
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
