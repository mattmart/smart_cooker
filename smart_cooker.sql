--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: t_sc_timing; Type: TABLE; Schema: public; Owner: cooker; Tablespace: 
--

CREATE TABLE t_sc_timing (
    sc_id integer NOT NULL,
    curr_temp numeric,
    ts timestamp with time zone DEFAULT now() NOT NULL,
    target_temp numeric,
    uuid character varying(255),
    CONSTRAINT t_sc_timing_target_temp_check CHECK (((target_temp > (0)::numeric) AND (target_temp < (100)::numeric))),
    CONSTRAINT t_sc_timing_temp_check CHECK (((curr_temp > (0)::numeric) AND (curr_temp < (100)::numeric)))
);


ALTER TABLE public.t_sc_timing OWNER TO cooker;

--
-- Name: t_slowcookers; Type: TABLE; Schema: public; Owner: cooker; Tablespace: 
--

CREATE TABLE t_slowcookers (
    sc_id integer NOT NULL,
    cooker_name character varying(255),
    description character varying(255)
);


ALTER TABLE public.t_slowcookers OWNER TO cooker;

--
-- Name: t_sc_timing_primary_key; Type: CONSTRAINT; Schema: public; Owner: cooker; Tablespace: 
--

ALTER TABLE ONLY t_sc_timing
    ADD CONSTRAINT t_sc_timing_primary_key PRIMARY KEY (sc_id, ts);


--
-- Name: t_slowcookers_pkey; Type: CONSTRAINT; Schema: public; Owner: cooker; Tablespace: 
--

ALTER TABLE ONLY t_slowcookers
    ADD CONSTRAINT t_slowcookers_pkey PRIMARY KEY (sc_id);


--
-- Name: t_sc_timing_sc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cooker
--

ALTER TABLE ONLY t_sc_timing
    ADD CONSTRAINT t_sc_timing_sc_id_fkey FOREIGN KEY (sc_id) REFERENCES t_slowcookers(sc_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

