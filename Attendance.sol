// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attendance {
    struct Student {
        uint id;
        string name;
        bool present;
    }

    mapping(uint => Student) public students;
    uint public studentCount;

    event StudentAdded(uint id, string name);
    event AttendanceMarked(uint id, bool present);

    function addStudent(string memory _name) public {
        studentCount++;
        students[studentCount] = Student(studentCount, _name, false);
        emit StudentAdded(studentCount, _name);
    }

    function markAttendance(uint _id, bool _present) public {
        require(_id > 0 && _id <= studentCount, "Student ID is invalid");
        students[_id].present = _present;
        emit AttendanceMarked(_id, _present);
    }

    function getStudent(uint _id) public view returns (uint, string memory, bool) {
        require(_id > 0 && _id <= studentCount, "Student ID is invalid");
        Student memory s = students[_id];
        return (s.id, s.name, s.present);
    }
}
