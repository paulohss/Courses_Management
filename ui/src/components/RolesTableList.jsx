import axios from 'axios';
import { useState, useEffect } from 'react';

export default function RolesTableList({ handleOpen, searchTerm, refreshTable, setRefreshTable }) {

    const [roleTable, setRoleTable] = useState([]); // State for Role Table
    const [error, setError] = useState(null);       // State for Error

    //--------------------------------------------------------------------------------
    // Fetch the roles from the API
    //--------------------------------------------------------------------------------
    const fetchRoles = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/roles');
            setRoleTable(response.data);
        } catch (error) {
            setError(error);
        }
    };

    //--------------------------------------------------------------------------------
    // Fetch the roles from the API
    //--------------------------------------------------------------------------------
    useEffect(() => {
        fetchRoles();
    }, []);

    useEffect(() => {
        if (refreshTable) {
            fetchRoles();
            setRefreshTable(false);
        }
    }, [refreshTable, setRefreshTable]);

    //--------------------------------------------------------------------------------
    // Filter the roleTable based on the search term
    //--------------------------------------------------------------------------------
    const filteredData = roleTable.filter(role => 
        role.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    //--------------------------------------------------------------------------------
    // Function to delete a role
    //--------------------------------------------------------------------------------
    const handleDelete = async (id) => {
        const confirm = window.confirm('Are you sure you want to delete this role?');
        if (!confirm) return;
        try {
            console.log('Deleting role with id:', id);
            await axios.delete(`http://localhost:5000/api/roles/${id}`);
            setRoleTable(roleTable.filter(role => role.id !== id));
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
                            <th>ROLE TITLE</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredData.map((role) => (
                            <tr className="hover" key={role.id}>
                                <th>{role.id}</th>
                                <td>{role.name}</td>
                                <td>
                                    <button className="btn btn-secondary" onClick={() => handleOpen('edit', role)}>Update</button>
                                </td>
                                <td>
                                    <button className="btn btn-accent" onClick={() => handleDelete(role.id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}