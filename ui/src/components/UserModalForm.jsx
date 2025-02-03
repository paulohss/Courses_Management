import { useState, useEffect } from "react";
import axios from 'axios';


// ModalForm.js 
export default function UserModalForm({ isOpen, onClose, mode, onSubmit, userData }) {

    const [id, setId] = useState(''); // State for Name
    const [name, setName] = useState(''); // State for Name
    const [roleId, setRoleId] = useState(''); // State for Role ID
    const [roles, setRoles] = useState([]); // State for Roles LIST
    const [userCourses, setUserCourses] = useState([]); // State for User Courses
    const [shouldClose, setShouldClose] = useState(true); // State to close the modal
    const [message, setMessage] = useState(''); // Add new state for message

    //--------------------------------------------------------------------------------
    // Function to cleanup form fields
    //--------------------------------------------------------------------------------
    const cleanupFields = () => {
        setId('');
        setName('');
        setRoleId('');
        setUserCourses([]);
    };

    //--------------------------------------------------------------------------------
    // Function to handle modal close
    //--------------------------------------------------------------------------------
    const handleClose = () => {
        cleanupFields();
        onClose();
    };    

    //--------------------------------------------------------------------------------
    // Function to handle form submission
    //--------------------------------------------------------------------------------
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("ModalForm.handleSubmit() mode:" + mode);
            const newUserData = { name, role_id: Number(roleId) };
            console.log(newUserData)
            await onSubmit(newUserData);
        } catch (error) {
            console.error("ModalForm.handleSubmit() error:" + error);
        }
        if (shouldClose)
            onClose();
    }

    //--------------------------------------------------------------------------------
    // Fetch roles from the API
    //--------------------------------------------------------------------------------
    const fetchRoles = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/roles');
            setRoles(response.data);
        } catch (error) {
            console.error('Error fetching roles', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch user data including courses from the API by user ID (Edit User)
    //--------------------------------------------------------------------------------
    const fetchUserData = async (userId) => {
        try {
            const response = await axios.get(`http://localhost:5000/api/users/${userId}`);
            const user = response.data;
            setId(user.id);
            setName(user.name);
            setRoleId(user.role.id);
            setUserCourses(user.userCourseList);
        } catch (error) {
            console.error('Error fetching user data', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch courses by role ID from the API (New User)
    //--------------------------------------------------------------------------------
    const fetchCoursesByRoleId = async (roleId) => {
        try {
            console.log("roleId:" + roleId);
            const response = await axios.get(`http://127.0.0.1:5000/api/role_courses/role/${roleId}`);
            setUserCourses(response.data);
        } catch (error) {
            console.error('Error fetching courses by role ID', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Handle course button click
    //--------------------------------------------------------------------------------
    const handleCourseButtonClick = async (courseId, attended) => {
        setShouldClose(false); // Prevent the modal from closing
        try {
            if (mode === 'edit') {
                if (attended) {
                    await axios.delete(`http://localhost:5000/api/user_courses`, {
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        data: { user_id: id, course_id: courseId }
                    });
                } else {
                    await axios.post(`http://localhost:5000/api/user_courses`, { user_id: id, course_id: courseId }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }
                fetchUserData(id);// Refresh user data
            } else {
                setMessage('Please save the User first!');
                // Clear message after 3 seconds
                setTimeout(() => setMessage(''), 3000);
            }
        } catch (error) {
            console.error('Error updating course attendance', error);
        }
    };

    //--------------------------------------------------------------------------------------
    // useEffect | to set the form fields when in edit mode - or clear them when in add mode
    //--------------------------------------------------------------------------------------
    useEffect(() => {
        // EDIT MODE
        if (mode === 'edit' && userData) {
            fetchRoles();
            console.log("ModalForm.useEffect() mode:" + mode);
            console.log(userData);
            fetchUserData(userData.id);
        }
        // ADD MODE
        else {
            console.log("ModalForm.useEffect() mode:" + mode);
            console.log(userData);
            cleanupFields();
        }
    }, [mode, userData]);

    //--------------------------------------------------------------------------------------
    // useEffect | to fetch courses by role ID when roleId changes in add mode
    //--------------------------------------------------------------------------------------
    useEffect(() => {
        console.log("mode and roleId:" + mode + " " + roleId);
        if (mode === 'add' && roleId) {
            fetchCoursesByRoleId(roleId);
        }
    }, [roleId, mode]);

    return (
        <>

            <dialog id="my_modal_3" className="modal bg-black/40" open={isOpen}>
                <div className="modal-box">
                    {/* if there is a button in form, it will close the modal */}
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={handleClose}>✕</button>
                    <h3 className="font-bold text-lg py-4">{mode === 'edit' ? 'Edit User' : 'User Details'}</h3>

                    <form onSubmit={handleSubmit}>

                        {/* Field: NAME */}
                        <label className="input input-bordered flex items-center my-4 gap-2">
                            Name
                            <input type="text" className="grow" value={name} onChange={(e) => setName(e.target.value)} />
                        </label>

                        {/* Field: ROLE */}
                        <div className="flex mb-4 justify-between">
                            <select className="select select-bordered w-full max-w-xs" value={roleId} onChange={(e) => setRoleId(e.target.value)}>
                                <option value="">Select Role</option>
                                {roles.map(role => (
                                    <option key={role.id} value={role.id}>{role.name}</option>
                                ))}
                            </select>
                        </div>

                        {/*Table: COURSES */}
                        {mode === 'edit' && userCourses.length > 0 && (
                            <div className="overflow-x-auto mt-4">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Recurrent</th>
                                            <th>Attended</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {userCourses.map((course) => (
                                            <tr className="hover" key={course.id}>
                                                <td>{course.name}</td>
                                                <td>{course.recurrent}</td>
                                                <td>
                                                    <button
                                                        className={course.attended ? 'btn btn-success' : 'btn btn-active btn-neutral'}
                                                        onClick={() => handleCourseButtonClick(course.id, course.attended)}
                                                    >
                                                        {course.attended ? 'Yes' : 'No'}
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}

                        {/* Button: SUBMIT and CLOSE */}
                        <div className="flex justify-between mt-4">
                            <button type="submit" className="btn btn-success" onClick={() => setShouldClose(true)}>
                                {mode === 'edit' ? 'Save Changes' : 'Add User'}
                            </button>
                            <button type="button" className="btn btn-outline btn-primary" onClick={handleClose}>
                                Close
                            </button>
                        </div>
                    </form>
                </div>
            </dialog>

        </>

    );
}