import { useState, useEffect } from "react";
import axios from 'axios';

export default function RolesModalForm({ isOpen, onClose, mode, onSubmit, roleData }) {

    const [id, setId] = useState(''); // State for ID
    const [name, setName] = useState(''); // State for Name
    const [courses, setCourses] = useState([]); // State for Courses linked to the Role
    const [shouldClose, setShouldClose] = useState(true); // State to close the modal

    //--------------------------------------------------------------------------------
    // Function to handle form submission
    //--------------------------------------------------------------------------------
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("RolesModalForm.handleSubmit() mode:" + mode);
            const newRoleData = { name };
            console.log(newRoleData)
            await onSubmit(newRoleData);
        } catch (error) {
            console.error("RolesModalForm.handleSubmit() error:" + error);
        }
        if (shouldClose)
            onClose();
    }

    //--------------------------------------------------------------------------------
    // Fetch role data including courses from the API by role ID (Edit Role)
    //--------------------------------------------------------------------------------
    const fetchRoleData = async (roleId) => {
        try {
            const response = await axios.get(`http://localhost:5000/api/roles/${roleId}`);
            const role = response.data;
            setId(role.id);
            setName(role.name);
            setCourses(role.coursesList);
        } catch (error) {
            console.error('Error fetching role data', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch all courses from the API (New Role)
    //--------------------------------------------------------------------------------
    const fetchAllCourses = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/courses');
            setCourses(response.data);
        } catch (error) {
            console.error('Error fetching courses', error);
        }
    };

    //--------------------------------------------------------------------------------
    // Handle course button click
    //--------------------------------------------------------------------------------
    const handleCourseButtonClick = async (courseId, linked) => {
        setShouldClose(false); // Prevent the modal from closing
        try {
            if (linked) {
                await axios.delete(`http://localhost:5000/api/role_courses`, {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: { role_id: id, course_id: courseId }
                });
            } else {
                await axios.post(`http://localhost:5000/api/role_courses`, { role_id: id, course_id: courseId }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            }
            // Refresh role data
            if (mode === 'edit') {
                fetchRoleData(id);
            } else {
                fetchAllCourses();
            }
        } catch (error) {
            console.error('Error updating course linkage', error);
        }
    };

    //--------------------------------------------------------------------------------------
    // useEffect | to set the form fields when in edit mode - or clear them when in add mode
    //--------------------------------------------------------------------------------------
    useEffect(() => {
        if (mode === 'edit' && roleData) {
            console.log("RolesModalForm.useEffect() mode:" + mode);
            console.log(roleData);
            fetchRoleData(roleData.id);
        }
        else {
            console.log("RolesModalForm.useEffect() mode:" + mode);
            console.log(roleData);
            setId('');
            setName('');
            setCourses([]);
            fetchAllCourses();
        }
    }, [mode, roleData]);

    return (
        <>

            <dialog id="my_modal_3" className="modal bg-black/40" open={isOpen}>
                <div className="modal-box">
                    {/* if there is a button in form, it will close the modal */}
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>✕</button>
                    <h3 className="font-bold text-lg py-4">{mode === 'edit' ? 'Edit Role' : 'Role Details'}</h3>

                    <form onSubmit={handleSubmit}>

                        {/* Field: NAME */}
                        <label className="input input-bordered flex items-center my-4 gap-2">
                            Name
                            <input type="text" className="grow" value={name} onChange={(e) => setName(e.target.value)} />
                        </label>

                        {/*Table: COURSES */}
                        {courses.length > 0 && (
                            <div className="overflow-x-auto mt-4">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Recurrent</th>
                                            <th>Linked</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {courses.map((course) => (
                                            <tr className="hover" key={course.id}>
                                                <td>{course.name}</td>
                                                <td>{course.recurrent}</td>
                                                <td>
                                                    <button
                                                        className={course.linked ? 'btn btn-success' : 'btn btn-active btn-neutral'}
                                                        onClick={() => handleCourseButtonClick(course.id, course.linked)}
                                                    >
                                                        {course.linked ? 'Yes' : 'No'}
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
                                {mode === 'edit' ? 'Save Changes' : 'Add Role'}
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