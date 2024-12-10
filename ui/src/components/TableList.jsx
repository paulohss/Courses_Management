import axios from 'axios';
import { useState, useEffect } from 'react';

export default function TableList({handleOpen, searchTerm}) {

    const [userTable, setUserTable] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/users');
                setUserTable(response.data);
            } catch (error) {
                setError(error);
            }
        };
        fetchUsers();

    }, [])

    const filteredData = userTable.filter(user => 
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        user.role.name.toLowerCase().includes(searchTerm.toLowerCase()) 
    );

    return (
        <>
            {error && <div className="alert alert-error">An error occurred: {error.message}</div>}

            <div className="overflow-x-auto mt-10">
                <table className="table">
                    {/* head */}
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Role</th>
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
                                    <button className="btn btn-secondary " onClick={()=>handleOpen('edit')}>Update</button>
                                </td>
                                <td>
                                    <button className="btn btn-accent">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}