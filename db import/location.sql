--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.20
-- Dumped by pg_dump version 9.6.20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: work; Type: TABLE; Schema: public; Owner: nomli
--

CREATE TABLE public.work (
    "time" timestamp without time zone,
    source_id integer,
    priority integer,
    name character varying,
    weight double precision,
    data real,
    text character varying
);


ALTER TABLE public.work OWNER TO nomli;

--
-- Data for Name: work; Type: TABLE DATA; Schema: public; Owner: nomli
--

COPY public.work ("time", source_id, priority, name, weight, data, text) FROM stdin;
2022-02-23 07:28:58	1	1	foobar	21.1119999999999983	34.3333321	foobar barfoo foobar foo bar
2022-02-14 08:30:13	2	334	barfoo	12.2210000000000001	43.4444427	boofar far foo boo bar barfoo
2022-03-01 11:23:58	4	2	fff	2122	33	foo
2022-03-01 09:53:36	3	2	foo	21.2220000000000013	34.3333321	foobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffd
2022-03-01 09:53:36	3	2	foo	21.2220000000000013	34.3333321	foobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffd
2022-03-01 09:53:36	3	2	foo	21.2220000000000013	34.3333321	foobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffd
2022-03-01 09:53:36	3	2	foo	21.2220000000000013	34.3333321	foobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffd
2022-03-01 09:53:36	3	2	foo	21.2220000000000013	34.3333321	foobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffdfoobar foofoo bar foo bar bar foo foo bar foobar barfoo foobar dsaaaaaaaaaaaaaaaaaasssssssssssssssssssssssssssssssssssssssffffffffffffffffffffffffffffffffffffffffffffffffffd
2022-03-01 11:23:58	4	2	fff	2122	33	foo
\.


--
-- PostgreSQL database dump complete
--

