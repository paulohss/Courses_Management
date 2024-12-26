import axios from 'axios';
import { useState, useEffect } from 'react';

export default function CoursesTableList({ handleOpen, searchTerm, refreshTable, setRefreshTable }) {

    const [courseTable, setCourseTable] = useState([]); // State for Course Table
    const [error, setError] = useState(null);           // State for Error

    //--------------------------------------------------------------------------------
    // Fetch the courses from the API
    //--------------------------------------------------------------------------------
    const fetchCourses = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/courses');
            setCourseTable(response.data);
        } catch (error) {
            setError(error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch the courses from the API
    //--------------------------------------------------------------------------------
    useEffect(() => {
        fetchCourses();
    }, []);

    useEffect(() => {
        if (refreshTable) {
            fetchCourses();
            setRefreshTable(false);
        }
    }, [refreshTable, setRefreshTable]);

    //--------------------------------------------------------------------------------
    // Filter the courseTable based on the search term
    //--------------------------------------------------------------------------------
    const filteredData = courseTable.filter(course => 
        course.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    //--------------------------------------------------------------------------------
    // Function to delete a course
    //--------------------------------------------------------------------------------
    const handleDelete = async (id) => {
        const confirm = window.confirm('Are you sure you want to delete this course?');
        if (!confirm) return;
        try {
            console.log('Deleting course with id:', id);
            await axios.delete(`http://localhost:5000/api/courses/${id}`);
            setCourseTable(courseTable.filter(course => course.id !== id));
        } catch (error) {
            setError(error);
        }
    };

    return (
        <>
            {error && <div className="alert alert-error">An error occurred: {error.message}</div>}

            <div className="overflow-x-auto mt-10">
                <table className="table">
                    {/* head */}
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>COURSE TITLE</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredData.map((course) => (
                            <tr className="hover" key={course.id}>
                                <th>{course.id}</th>
                                <td>{course.name}</td>
                                <td>
                                    <button className="btn btn-secondary" onClick={() => handleOpen('edit', course)}>Update</button>
                                </td>
                                <td>
                                    <button className="btn btn-accent" onClick={() => handleDelete(course.id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}