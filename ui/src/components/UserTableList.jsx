import axios from 'axios';
import { useState, useEffect } from 'react';  

export default function UserTableList({handleOpen, searchTerm, refreshTable, setRefreshTable}) {
    
    const [userTable, setUserTable] = useState([]); // State for User Table
    const [error, setError] = useState(null);       // State for Error

    //--------------------------------------------------------------------------------
    // Fetch the users from the API
    //--------------------------------------------------------------------------------
    const fetchUsers = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/users');
            setUserTable(response.data);
        } catch (error) {
            setError(error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch the users from the API
    //--------------------------------------------------------------------------------
    useEffect(() => {
        fetchUsers();
    }, []);

    useEffect(() => {
        if (refreshTable) {
            fetchUsers();
            setRefreshTable(false);
        }
    }, [refreshTable, setRefreshTable]);

    //--------------------------------------------------------------------------------
    // Filter the userTable based on the search term
    //--------------------------------------------------------------------------------
    const filteredData = userTable.filter(user => 
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        user.role.name.toLowerCase().includes(searchTerm.toLowerCase()) 
    );

    //--------------------------------------------------------------------------------
    // Function to delete a user
    //--------------------------------------------------------------------------------
    const handleDelete = async (id) => {
        const confirm = window.confirm('Are you sure you want to delete this user?');
        if (!confirm) return;
        try {
            console.log('Deleting user with id:', id);
            await axios.delete(`http://localhost:5000/api/users/${id}`);
            setUserTable(userTable.filter(user => user.id !== id));
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
                            <th>NAME</th>
                            <th>ROLE</th>
                        </tr>
                    </thead>
                    <tbody>
                        { }
                        {filteredData.map((user) => (
                            <tr className="hover" key={user.id}>
                                <th>{user.id}</th>
                                <td>{user.name}</td>
                                <td>{user.role.name}</td>
                                <td>
                                    <button className="btn btn-secondary " onClick={()=>handleOpen('edit', user)}>Update</button>
                                </td>
                                <td>
                                    <button className="btn btn-accent" onClick={()=> handleDelete(user.id)} >Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}