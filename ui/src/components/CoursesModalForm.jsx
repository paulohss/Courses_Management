import { useState, useEffect } from "react";
import axios from 'axios';

export default function CoursesModalForm({ isOpen, onClose, mode, onSubmit, courseData }) {

    const [id, setId] = useState(''); // State for ID
    const [name, setName] = useState(''); // State for Name
    const [recurrent, setRecurrent] = useState(''); // State for Recurrent
    const [roles, setRoles] = useState([]); // State for Roles linked to the Course
    const [shouldClose, setShouldClose] = useState(true); // State to close the modal

    //--------------------------------------------------------------------------------
    // Function to handle form submission
    //--------------------------------------------------------------------------------
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("CoursesModalForm.handleSubmit() mode:" + mode);
            const newCourseData = { name, recurrent };
            console.log(newCourseData)
            await onSubmit(newCourseData);
        } catch (error) {
            console.error("CoursesModalForm.handleSubmit() error:" + error);
        }
        if (shouldClose)
            onClose();
    }

    //--------------------------------------------------------------------------------
    // Fetch course data including roles from the API by course ID (Edit Course)
    //--------------------------------------------------------------------------------
    const fetchCourseData = async (courseId) => {
        try {
            const response = await axios.get(`http://localhost:5000/api/courses/${courseId}`);
            const course = response.data;
            setId(course.id);
            setName(course.name);
            setRecurrent(course.recurrent);
            setRoles(course.rolesList);
        } catch (error) {
            console.error('Error fetching course data', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch all roles from the API (New Course)
    //--------------------------------------------------------------------------------
    const fetchAllRoles = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/roles');
            setRoles(response.data);
        } catch (error) {
            console.error('Error fetching roles', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Handle role button click
    //--------------------------------------------------------------------------------
    const handleRoleButtonClick = async (roleId, linked) => {
        setShouldClose(false); // Prevent the modal from closing
        console.log('Role button clicked:', id, roleId, linked);
        try {
            if (linked) {
                await axios.delete(`http://localhost:5000/api/role_courses`, {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: { course_id: id, role_id: roleId }
                });
            } else {
                await axios.post(`http://localhost:5000/api/role_courses`, { course_id: id, role_id: roleId }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            }
            // Refresh course data
            if (mode === 'edit') {
                fetchCourseData(id);
            } else {
                fetchAllRoles();
            }
        } catch (error) {
            console.error('Error updating role linkage', error);
        }
    };

    //--------------------------------------------------------------------------------------
    // useEffect | to set the form fields when in edit mode - or clear them when in add mode
    //--------------------------------------------------------------------------------------
    useEffect(() => {
        if (mode === 'edit' && courseData) {
            console.log("CoursesModalForm.useEffect() mode:" + mode);
            console.log(courseData);
            fetchCourseData(courseData.id);
        }
        else {
            console.log("CoursesModalForm.useEffect() mode:" + mode);
            console.log(courseData);
            setId('');
            setName('');
            setRecurrent('None');
            setRoles([]);
            fetchAllRoles();
        }
    }, [mode, courseData]);

    return (
        <>

            <dialog id="my_modal_3" className="modal bg-black/40" open={isOpen}>
                <div className="modal-box">
                    {/* if there is a button in form, it will close the modal */}
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
                    <h3 className="font-bold text-lg py-4">{mode === 'edit' ? 'Edit Course' : 'Course Details'}</h3>

                    <form onSubmit={handleSubmit}>

                        {/* Field: NAME */}
                        <label className="input input-bordered flex items-center my-4 gap-2">
                            Name
                            <input type="text" className="grow" value={name} onChange={(e) => setName(e.target.value)} />
                        </label>

                        {/* Field: RECURRENT */}
                        <label className="input input-bordered flex items-center my-4 gap-2">
                            Recurrent
                            <select className="grow" value={recurrent} onChange={(e) => setRecurrent(e.target.value)}>
                                <option value="Annual">Annual</option>
                                <option value="None">None</option>
                            </select>
                        </label>

                        {/*Table: ROLES */}
                        {roles.length > 0 && (
                            <div className="overflow-x-auto mt-4">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Linked</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {roles.map((role) => (
                                            <tr className="hover" key={role.id}>
                                                <td>{role.name}</td>
                                                <td>
                                                    <button
                                                        className={role.linked ? 'btn btn-success' : 'btn btn-active btn-neutral'}
                                                        onClick={() => handleRoleButtonClick(role.id, role.linked)}
                                                    >
                                                        {role.linked ? 'Yes' : 'No'}
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
                                {mode === 'edit' ? 'Save Changes' : 'Add Course'}
                            </button>
                            <button type="button" className="btn btn-outline btn-primary" onClick={onClose}>
                                Close
                            </button>
                        </div>
                    </form>
                </div>
            </dialog>

        </>

    );
}