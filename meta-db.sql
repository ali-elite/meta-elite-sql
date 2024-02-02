-- Create custom ENUM type for IndexType
CREATE TYPE index_type AS ENUM ('PRIMARY', 'UNIQUE', 'INDEX');

-- Create Tables table
CREATE TABLE Tables (
    TableID SERIAL PRIMARY KEY,
    TableName VARCHAR(255) NOT NULL,
    Description TEXT
);

-- Create Columns table
CREATE TABLE Columns (
    ColumnID SERIAL PRIMARY KEY,
    TableID INT,
    ColumnName VARCHAR(255) NOT NULL,
    DataType VARCHAR(100),
    IsNullable BOOLEAN,
    DefaultValue VARCHAR(255),
    FOREIGN KEY (TableID) REFERENCES Tables(TableID)
);

-- Create Constraints table
CREATE TYPE constraint_type AS ENUM ('PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK');

CREATE TABLE Constraints (
    ConstraintID SERIAL PRIMARY KEY,
    TableID INT,
    ColumnID INT,
    ConstraintType constraint_type,
    ReferenceTableID INT NULL,
    ReferenceColumnID INT NULL,
    CheckCondition TEXT NULL,
    FOREIGN KEY (TableID) REFERENCES Tables(TableID),
    FOREIGN KEY (ColumnID) REFERENCES Columns(ColumnID),
    FOREIGN KEY (ReferenceTableID) REFERENCES Tables(TableID),
    FOREIGN KEY (ReferenceColumnID) REFERENCES Columns(ColumnID)
);

-- Create Indexes table
CREATE TABLE Indexes (
    IndexID SERIAL PRIMARY KEY,
    TableID INT,
    ColumnID INT,
    IndexType index_type,
    FOREIGN KEY (TableID) REFERENCES Tables(TableID),
    FOREIGN KEY (ColumnID) REFERENCES Columns(ColumnID)
);

-- Create Relationships table
CREATE TABLE Relationships (
    RelationshipID SERIAL PRIMARY KEY,
    ForeignKeyTableID INT,
    ForeignKeyColumnID INT,
    PrimaryKeyTableID INT,
    PrimaryKeyColumnID INT,
    FOREIGN KEY (ForeignKeyTableID) REFERENCES Tables(TableID),
    FOREIGN KEY (ForeignKeyColumnID) REFERENCES Columns(ColumnID),
    FOREIGN KEY (PrimaryKeyTableID) REFERENCES Tables(TableID),
    FOREIGN KEY (PrimaryKeyColumnID) REFERENCES Columns(ColumnID)
);
