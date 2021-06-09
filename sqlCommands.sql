
-- UPDATE OWN_TODO_LIST SET TaskTitle='testing modify action', ToDueDate='2021-06-25' WHERE taskID=6;

-- UPDATE own_todo_list set DoneBy=1 where DoneBy=0;


-- select ToDueDate from own_todo_list;

-- INSERT INTO OWN_TODO_LIST (TaskTitle, TaskDesc, CreatedBy, ToDueDate) VALUES ('kk 2', 'NOT USED', 0, '2021-06-04');

--  select * from own_todo_list;

-- update own_todo_list set DoneBy=0 where taskID=1;

-- UPDATE OWN_TODO_TASK SET DoneBy=0 WHERE taskID=8;

-- show columns in own_todo_list;


/* 
CREATE TABLE list_home (
	taskID int not null AUTO_INCREMENT,
	taskTitle varchar(50) not null,
	ToDueDate DATETIME, 
	CreatedBy int, 
	DoneBy int, 
	PRIMARY KEY (taskID)); */

	show tables;