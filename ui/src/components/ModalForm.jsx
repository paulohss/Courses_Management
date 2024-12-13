import { useState, useEffect } from "react";
import axios from 'axios';

// ModalForm.js
export default function ModalForm({ isOpen, onClose, mode, onSubmit, userData }) {
    
    const [id, setId] = useState(''); // State for Name
    const [name, setName] = useState(''); // State for Name
    const [roleId, setRoleId] = useState(''); // State for Role ID
    const [roles, setRoles] = useState([]); // State for Roles LIST

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            console.log("ModalForm.handleSubmit() mode:" + mode);
            const newUserData = {name, role_id: Number(roleId) };
            console.log(newUserData)
            await onSubmit(newUserData);
        } catch (error) {
            console.error("ModalForm.handleSubmit() error:" + error);
        }
        onClose();
    }


    // Fetch roles from the API
    const fetchRoles = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/roles');
            setRoles(response.data);
        } catch (error) {
            console.error('Error fetching roles', error);
        }
    };    

    // useEffect to set the form fields when in edit mode - or clear them when in add mode
    useEffect(() => {
        fetchRoles();        
        if (mode === 'edit' && userData) {
            console.log("ModalForm.useEffect() mode:" + mode);
            console.log(userData);
            setId(userData.id);
            setName(userData.name);
            setRoleId(userData.role.id);
        }
        else {
            console.log("ModalForm.useEffect() mode:" + mode);
            console.log(userData);
            setId('');
            setName('');
            setRoleId('');
        }
    }, [mode, userData]);


    return (
        <>

            <dialog id="my_modal_3" className="modal bg-black/40" open={isOpen}>
                <div className="modal-box">
                    {/* if there is a button in form, it will close the modal */}
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
                    <h3 className="font-bold text-lg py-4">{mode === 'edit' ? 'Edit User' : 'User Details'}</h3>

                    <form onSubmit={handleSubmit}>

                        <label className="input input-bordered flex items-center my-4 gap-2">
                            Name
                            <input type="text" className="grow" value={name} onChange={(e) => setName(e.target.value)} />
                        </label>
                        <div className="flex mb-4 justify-between">
                        <select className="select select-bordered w-full max-w-xs" value={roleId} onChange={(e) => setRoleId(e.target.value)}>
                                <option value="">Select Role</option>
                                {roles.map(role => (
                                    <option key={role.id} value={role.id}>{role.name}</option>
                                ))}
                            </select>
                        </div>
                        <button type="submit" className=" btn btn-success">{mode === 'edit' ? 'Save Changes' : 'Add User'}</button>
                    </form>
                </div>
            </dialog>

        </>

    );
}