DROP DATABASE IF EXISTS ProjectBD1_Backup;
CREATE DATABASE IF NOT EXISTS ProjectBD1_Backup CHARACTER SET utf8;
USE ProjectBD1_Backup;

CREATE TABLE IF NOT EXISTS DrawBackup(
    id INT AUTO_INCREMENT PRIMARY KEY,
    jso_compressedDraw JSON COMMENT "Almacena un JSON comprimido equivalente al que esta almacenado en la base ProjectBD1"
);