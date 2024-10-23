create table tUsuarios(
    id int primary key auto_increment,
    nombre varchar(50) not null, 
    apellidos varchar(100) not null,
    email varchar(200) unique not null,
    contraseña varchar(200) not null
);

insert into tUsuarios (nombre, apellidos, email, contraseña) values
('Juan', 'Pérez', 'juan.perez@example.com', 'contrasena123'),
('María', 'Gómez', 'maria.gomez@example.com', 'contrasena456'),
('Carlos', 'Ramírez', 'carlos.ramirez@example.com', 'contrasena789'),
('Ana', 'Martínez', 'ana.martinez@example.com', 'contrasena321'),
('Lucía', 'Fernández', 'jlucia.fernandez@example.com', 'contrasena654');

create table tPelículas(
    id int primary key auto_increment, 
    nombre varchar(50) not null,
    url_imagen varchar(200) not null,
    director varchar(100) not null,
    anio_estreno int not null
);

insert into tPeliculas (nombre, url_imagen, director, anio_estreno) values
('El padrino', 'https://es.web.img3.acsta.net/c_310_420/pictures/18/06/12/12/12/0117051.jpg?coixp=49&coiyp=27', 'Francis Ford Coppola', 1972),
('Inception', 'https://m.media-amazon.com/images/I/51a7hc58lDL._SX300_SY300_QL70_ML2_.jpg', 'Christoper Nolan', 2010),
('Matrix', 'https://pics.filmaffinity.com/the_matrix-155050517-mmed.jpg', 'Lana Wachowski, Lilly Wachowski', 1999),
('Interstellar', 'https://pics.filmaffinity.com/interstellar-366875261-mmed.jpg', 'Christopher Nolan', 2014),
('Parasite', 'https://media.vogue.mx/photos/5e1c9b80c851470009c2fd92/2:3/w_960,c_limit/parasite-nominada-premio-oscar.jpg', 'Bong Joon-ho', 2019);


create table tComentarios(
    id int primary key auto_increment,
    comentario varchar(2000) not null,
    usuario_id int,
    pelicula_id int not null,
    foreign key (usuario_id) references tUsuarios(id),
    foreign key (pelicula_id) references tPeliculas(id)
);


insert into tComentarios (comentario, usuario_id, pelicula_id) values
('Increíble película, una obbra maestra.',1, 1),
('Una película muy interesante y bien dirigida.',2, 2);
('Nunca había visto algo tan revolucionario.',3, 3),
('Una visión espectacular del futuro.'4, 4),
('La mejor película que he visto en años.', 5, 5),
('Inception es una película que te hace pensar.',1, 2),
('Me encantó la trama de Matrix.',2, 3);








