import { useState } from "react";


// ModalForm.js
export default function ModalForm({ isOpen, onClose, mode, onSubmit }) {
    
    const [name, setName] = useState(''); // State for Name
    const [role, setRole] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onClose();
    }

    return (
        <>

            <dialog id="my_modal_3" className="modal bg-black/40" open={isOpen}>
                <div className="modal-box">
                    {/* if there is a button in form, it will close the modal */}
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
                    <h3 className="font-bold text-lg py-4">{mode === 'edit' ? 'Edit User' : 'User Details'}</h3>

                    <form onSubmit={(e) => { handleSubmit }}>

                        <label className="input input-bordered flex items-center my-4 gap-2">
                            Name
                            <input type="text" className="grow" value={name} onChange={(e) => setName(e.target.value)} />
                        </label>
                        <div className="flex mb-4 justify-between">
                            <select className="select select-bordered w-full max-w-xs" value={role} onChange={(e) => setRole(e.target.value)}>
                                <option>Inactive</option>
                                <option>Active</option>
                            </select>

                        </div>
                        <button type="submit" className=" btn btn-success">{mode === 'edit' ? 'Save Changes' : 'Add User'}</button>
                    </form>
                </div>
            </dialog>

        </>

    );
}