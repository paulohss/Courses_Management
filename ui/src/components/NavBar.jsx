export default function NavBar({ onOpen, onSearch, onMenuChange, selectedMenu }) {

    //--------------------------------------------------------------------------------
    //  Function to handle search change
    //--------------------------------------------------------------------------------
    const handleSearchChange = (event) => {
        onSearch(event.target.value);
    };

    return (
        <>
            <div className="navbar bg-base-100 p-4">
                <div className="navbar-start">
                    <ul className="menu bg-base-200 rounded-box w-56">
                        <li>
                            <h2 className="menu-title">Course Management</h2>
                            <ul>
                                <li><a onClick={() => onMenuChange('users')}>Users</a></li>
                                <li><a onClick={() => onMenuChange('roles')}>Roles</a></li>
                                <li><a onClick={() => onMenuChange('courses')}>Courses</a></li>
                                <li><a onClick={() => onMenuChange('chatbot')}>ChatBot</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
                <div className="navbar-center">
                    <div className="form-control">
                        <input type="text" placeholder="Search" onChange={handleSearchChange} className="input input-bordered w-48 md:w-auto" />
                    </div>
                </div>
                <div className="navbar-end">
                    <a className="btn btn-primary ml-2" onClick={() => onOpen('add')}>
                        {selectedMenu === 'users' ? 'Add User' :
                            selectedMenu === 'roles' ? 'Add Role' :
                                selectedMenu === 'courses' ? 'Add Course' : ''}
                    </a>
                </div>
            </div>
        </>
    );
}