DROP FUNCTION IF EXISTS getTopActors;
CREATE OR REPLACE FUNCTION getTopActors(g VARCHAR(128)) 
    RETURNS TABLE(actorname VARCHAR(128),
                  num_movies BIGINT,
                  debut TEXT,
                  title VARCHAR(128),
                  id INTEGER,
                  director TEXT)
    AS $$
    BEGIN
        RETURN QUERY(SELECT AC.actorname AS actorname,
                            AUX_COUNT.numMovies AS num_movies,
                            MIN(AUX_MOVIE.debut) AS debut,
                            AUX_MOVIE.movietitle AS title,
                            AUX_MOVIE.movieid AS id,
                            AUX_MOVIE.directorname AS director
                     FROM imdb_actors AS AC,
                          (SELECT AC.actorid AS actorid,
                                  count(AM.movieid) AS numMovies,
                                  MG.genre
                           FROM imdb_movies NATURAL JOIN
                                imdb_actormovies AS AM NATURAL JOIN
                                imdb_actors AS AC NATURAL JOIN
                                imdb_moviegenres AS MG
                                WHERE MG.genre = g
                                GROUP BY AC.actorid, MG.genre
                                ORDER BY numMovies DESC) AS AUX_COUNT,
                          (SELECT AM.actorid AS actorid,
                                  AUX_DEBUT.debut AS debut,
                                  MV.movietitle AS movietitle,
                                  MV.movieid AS movieid,
                                  CONCAT(DR.directorname) AS directorname
                           FROM (SELECT AM.actorid AS actorid,
                                        MIN(MV.year) AS debut,
                                        MG.genre
                                 FROM imdb_actormovies AS AM NATURAL JOIN
                                      imdb_movies AS MV NATURAL JOIN
                                      imdb_moviegenres AS MG
                                 WHERE MG.genre = g
                                 GROUP BY AM.actorid,
                                          MG.genre) AS AUX_DEBUT,
                                imdb_actormovies AS AM NATURAL JOIN
                                imdb_movies AS MV NATURAL JOIN
                                imdb_moviegenres AS MG NATURAL JOIN
                                imdb_directormovies NATURAL JOIN
                                imdb_directors AS DR
                           WHERE AUX_DEBUT.actorid = AM.actorid
                             AND AUX_DEBUT.debut = MV.year
                             AND MG.genre = g) AS AUX_MOVIE
                     WHERE AUX_COUNT.numMovies >= 4
                       AND AUX_COUNT.actorid = AC.actorid
                       AND AUX_MOVIE.actorid = AC.actorid
                     GROUP BY AC.actorname,
                              num_movies,
                              title,
                              id,
                              director
                     ORDER BY numMovies DESC);
    END;
$$ LANGUAGE plpgsql;
