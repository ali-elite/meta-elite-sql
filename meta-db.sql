-- Create ENUM types for index and constraint types
CREATE TYPE index_type AS ENUM ('PRIMARY', 'UNIQUE', 'INDEX');
CREATE TYPE constraint_type AS ENUM ('PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK');
CREATE TYPE relationship_degree AS ENUM ('ONE_TO_ONE', 'ONE_TO_MANY', 'MANY_TO_MANY');

-- Create Databases table
CREATE TABLE Databases (
    DatabaseID SERIAL PRIMARY KEY,
    DatabaseName VARCHAR(255) NOT NULL UNIQUE,
    Description TEXT
);

-- Create Schemas table
CREATE TABLE Schemas (
    SchemaID SERIAL PRIMARY KEY,
    DatabaseID INT NOT NULL,
    SchemaName VARCHAR(255) NOT NULL,
    Description TEXT,
    FOREIGN KEY (DatabaseID) REFERENCES Databases(DatabaseID) ON DELETE CASCADE,
    UNIQUE (DatabaseID, SchemaName)
);

-- Create Tables table
CREATE TABLE Tables (
    TableID SERIAL PRIMARY KEY,
    SchemaID INT NOT NULL,
    TableName VARCHAR(255) NOT NULL,
    Description TEXT,
    FOREIGN KEY (SchemaID) REFERENCES Schemas(SchemaID) ON DELETE CASCADE,
    UNIQUE (SchemaID, TableName)
);

-- Create Columns table
CREATE TABLE Columns (
    ColumnID SERIAL PRIMARY KEY,
    TableID INT NOT NULL,
    ColumnName VARCHAR(255) NOT NULL,
    DataType VARCHAR(100) NOT NULL,
    IsNullable BOOLEAN NOT NULL,
    DefaultValue VARCHAR(255),
    FOREIGN KEY (TableID) REFERENCES Tables(TableID) ON DELETE CASCADE,
    UNIQUE (TableID, ColumnName)
);

-- Create Constraints table
CREATE TABLE Constraints (
    ConstraintID SERIAL PRIMARY KEY,
    TableID INT NOT NULL,
    ColumnID INT NOT NULL,
    ConstraintType constraint_type NOT NULL,
    ReferenceTableID INT,
    ReferenceColumnID INT,
    CheckCondition TEXT,
    FOREIGN KEY (TableID) REFERENCES Tables(TableID) ON DELETE CASCADE,
    FOREIGN KEY (ColumnID) REFERENCES Columns(ColumnID) ON DELETE CASCADE,
    FOREIGN KEY (ReferenceTableID) REFERENCES Tables(TableID) ON DELETE SET NULL,
    FOREIGN KEY (ReferenceColumnID) REFERENCES Columns(ColumnID) ON DELETE SET NULL
);

-- Create Indexes table
CREATE TABLE Indexes (
    IndexID SERIAL PRIMARY KEY,
    TableID INT NOT NULL,
    ColumnID INT NOT NULL,
    IndexName VARCHAR(255) NOT NULL,
    IndexType index_type NOT NULL,
    FOREIGN KEY (TableID) REFERENCES Tables(TableID) ON DELETE CASCADE,
    FOREIGN KEY (ColumnID) REFERENCES Columns(ColumnID) ON DELETE CASCADE,
    UNIQUE (TableID, IndexName)
);

-- Create Relationships table
CREATE TABLE Relationships (
    RelationshipID SERIAL PRIMARY KEY,
    ForeignKeyTableID INT NOT NULL,
    ForeignKeyColumnID INT NOT NULL,
    PrimaryKeyTableID INT NOT NULL,
    PrimaryKeyColumnID INT NOT NULL,
    RelationshipDegree relationship_degree NOT NULL,
-- Optional: Reference to a join table for many-to-many relationships
    JoinTableID INT,
    FOREIGN KEY (ForeignKeyTableID) REFERENCES Tables(TableID) ON DELETE CASCADE,
    FOREIGN KEY (ForeignKeyColumnID) REFERENCES Columns(ColumnID) ON DELETE CASCADE,
    FOREIGN KEY (PrimaryKeyTableID) REFERENCES Tables(TableID) ON DELETE CASCADE,
    FOREIGN KEY (PrimaryKeyColumnID) REFERENCES Columns(ColumnID) ON DELETE CASCADE,
-- Optional: Foreign key constraint for the join table
    FOREIGN KEY (JoinTableID) REFERENCES Tables(TableID) ON DELETE CASCADE
);
