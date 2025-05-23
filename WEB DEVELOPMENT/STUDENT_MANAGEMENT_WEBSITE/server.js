const express = require('./node_modules/express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const multer = require('multer');
const upload = multer();
const fs = require('fs');
const fastcsv = require('fast-csv');
const path = require('path');
const app = express();
const port = 5500;
const os = require('os');
 
// console.log(path.join(__dirname,'..'*3));   // in join ..work / dont workin js     while / work and ..not in django

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(upload.array());
app.use('/static',express.static('public'));//here [['/static']] takes public dir.contents to server root with dir called static [[[else if server arg[1] not provided then arg[1]:default web path :'/]]]]'
// app.use(express.static('C:/Users/Windows/VS/HTML/PROJECTS/REG_FORM/public/'));
//(arg1,arg2) =====>>(mount webpath, sys file path)

// console.log(__dirname);   
// console.log(process.cwd());    


app.set('view engine','ejs')
app.set('views','./views')   //if not set to correct file path,by default it is initialized to cwd
// setting views to system views path ,so that while rendering prefix path is loaded C:..../views/{render path}
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'html'
});

db.connect((err) => {
    if (err) {
        throw err;
    }
});
app.get("",(req,res)=>{
    res.render("HTML/index.ejs")// loads prefix,arg was the string relative to views dir and not to current dir. 
})
app.get("/new/",(req,res)=>{
    res.render("HTML/new.ejs")
})
app.get("/edit/",(req,res)=>{
  res.render("HTML/edit.ejs")
})

app.post('/submit', (req, res) => {
    const name = req.body.Name;
    const roll_num = req.body.Roll;
    const stud_class = req.body.Class;
    const section = req.body.Section;

    const sql = 'INSERT INTO school (name, roll, stud_class, section) VALUES (?,?,?,?)';
    db.query(sql, [name, roll_num,stud_class,section], (err, result) => {
        if (err) {
            res.status(500).json({ message: 'Database error: ' + err });
            return;
        }
        res.json({ message: 'Form submitted successfully' });
    });
});


app.post('/rollvalidate_and_delete', (req, res) => {
  const roll_num = req.body.roll;
  const sql = 'SELECT * FROM school WHERE roll = ?';
  db.query(sql, [roll_num], (err, result) => {
      if (err) {
          res.status(500).json({ message: 'Database error: ' , flag: 0 });
          return;
      }
      if (result.length >= 1) {
        const sql1 = 'DELETE FROM school WHERE roll = ?';
        db.query(sql1,[roll_num],(err,response)=>{
          if (err) {
            res.status(500).json({ message: 'Database error: ', flag: 0 });
            return;
        }
        res.json({ message: 'RECORD DELETED', flag: 1,rnum: roll_num });
        })
      } else {
          res.json({ message: 'ROLL NUM NOT FOUND', flag: 0 });
      }
  });
});


app.get('/download',(req,res)=>{
    const sql = 'SELECT * FROM school ORDER BY stud_class, section, roll';
    db.query(sql, (err, results) => {
      if (err) {
        res.status(500).json({ message: 'Database error: ' + err });
        return;
      }
      const csvStream = fastcsv.format({ headers: true });
      res.setHeader('Content-disposition', 'attachment; filename=students.csv');
      res.setHeader('Content-Type', 'text/csv');
  
      csvStream.pipe(res);
      results.forEach(row => {
        csvStream.write(row);
      });
      csvStream.end();
    });
  });



app.get('/records/', (req, res) => { 
      res.render('HTML/records');
  });

app.post('/search-record', (req, res) => {
    const val = req.body.value;
    const sql = `
    SELECT * FROM school WHERE roll LIKE ? OR name LIKE ? OR section LIKE ? OR stud_class LIKE ?;
`;
const likeval = `${val}%`;
    db.query(sql, [likeval, likeval, likeval, likeval], (err, results) => {
        if (err) {
            res.status(500).json({ message: 'Database error: ' + err });
            return;
        }
        const groupedResults = groupResults(results);
        res.json(groupedResults);
    });
});  

app.post('/search-roll', (req, res) => {

    const val = req.body.value;
    const sql = `
    SELECT * FROM school WHERE roll LIKE ? ;
`;
    db.query(sql, [val], (err, results) => {
        if (err) {
            res.status(500).json({ message: 'Database error: ' + err });
            return;
        }
        if(results.length >=1){
        const groupedResults = {flag:1};
        res.json(groupedResults);}
        else{
            const groupedResults = {flag:0};
        res.json(groupedResults);
        }
    });
});  


app.get('/view-all-records', (req, res) => {
    const sql = 'SELECT * FROM school ORDER BY stud_class, section, roll';
    db.query(sql, (err, results) => {
        if (err) {
            res.status(500).json({ message: 'Database error: ' + err });
            return;
        }
        const groupedResults = groupResults(results);
        res.json(groupedResults);
    });
});


function groupResults(results) {
    const groupedResults = {};
    results.forEach(student => {
        if (!groupedResults[student.stud_class]) {
            groupedResults[student.stud_class] = {};
        }
        if (!groupedResults[student.stud_class][student.section]) {
            groupedResults[student.stud_class][student.section] = [];
        }
        groupedResults[student.stud_class][student.section].push({
            name: student.name,
            roll: student.roll
        });
    });
    return groupedResults;
}

app.post('/update-record', (req, res) => {
    const roll = req.body.roll;
    const newRoll = req.body.Roll;
    const newName = req.body.Name;
    const newClass = req.body.stud_class;
    const newSection = req.body.Section;
    if (!roll) {
        return res.status(400).json({ success: false, message: 'Original roll number is required.' });
    }
    let updates = [];
    let updateValues = [];

    if (newRoll) {
        updates.push('roll = ?');
        updateValues.push(newRoll);
    }
    if (newName) {
        updates.push('name = ?');
        updateValues.push(newName);
    }
    if (newClass) {
        updates.push('stud_class = ?');
        updateValues.push(newClass);
    }
    if (newSection) {
        updates.push('section = ?');
        updateValues.push(newSection);
    }
    updateValues.push(roll);

    const sql = `UPDATE school SET ${updates.join(', ')} WHERE roll = ?`;

    db.query(sql, updateValues, (err, results) => {
        if (err) {
            return res.status(500).json({ success: false, message: 'Database error: ' + err });
        }
        if (results.affectedRows === 0) {
            return res.status(404).json({ success: false, message: 'Roll number exists already' });
        }
        res.json({ success: true, message: 'Record updated successfully.' });
    });
});



app.listen(port, () => {
 
    console.log(`Server running at http://localhost:${port}`);
});
