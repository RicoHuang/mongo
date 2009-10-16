# See the file LICENSE for redistribution information.
#
# Copyright (c) 2008 WiredTiger Software.
#	All rights reserved.
#
# $Id$
#
# Auto-generate everything we can:
#	flag values
#	getter/setter code
#	manual page headers
#	structure method fields
#
# There are 3 primary handles: DB, ENV, and WT_TOC.  The DB and ENV handles are
# similar to Berkeley DB handles: DB is a single table/database, and ENV is a
# database/environment.   WiredTiger adds the WT_TOC handle, which identifies
# a single thread of control running in a single environment.  WiredTiger calls
# take a WT_TOC argument because the WT_TOC IDs the calling thread and caller's
# environment.
#
# Because the WT_TOC handle always references a single ENV, and to make the
# application "handler passing" problem simpler, we moved all the Berkeley DB
# methods into the WT_TOC structure (because otherwise we'd have ENV methods
# taking both ENV and WT_TOC arguments, or ENV methods that didn't take ENV
# arguments).   We could have left DB methods on the DB handle, but it seemed
# simpler to give the application fewer handles to pass around internally.
#
# The initial line of each entry in the api file:
#
#	handle.method name
#		<tab>flag[,flag]
#		<tab>argument	<tab>type
#
#	handles:
#		env	-- DbEnv handle
#		db	-- Db handle
#	tags:
#		getset  -- an API getter/setter method
#		local	-- no need to connect to the server[1]
#		method	-- a method returning an int
#		methodV -- a method returning void
#		open    -- illegal until after the handle.open method call
#		notoc	-- method doesn't take a WT_TOC reference
#		verify  -- setters call a subroutine to validate the arguments
#
# [1]
# Think carefully before marking API methods as "local".  The ENV/DB handles
# are free-threaded, and can be used concurrently (for example, one thread is
# calling Db.get while another thread is re-configuring the Db error prefix).
# A race is unlikely since most fields are 32-bit and updated atomically, and
# configuration is usually done once, before the handle is used (as one data
# point, Berkeley DB has the same problem and I don't believe I ever saw a
# failure in the field).  Regardless, handle configuration is a rarely done
# operation, so I don't see performance reasons for making more methods local.
#
# Subsequent lines are the argument names and declarations for the arguments;
# @S is replaced by the argument name in the declaration.  We do that because
# the name goes in different places in the declaration, and sometimes we want
# the name, and sometimes we don't.

env.open
	method
	home	const char *@S
	mode	mode_t @S
	flags	u_int32_t @S

env.close
	method
	flags	u_int32_t @S

env.db_create
	method
	flags	u_int32_t @S
	dbp	DB **@S

env.destroy
	method,local,notoc
	flags	u_int32_t @S

env.err
	methodV,local,notoc
	err	int @S
	fmt	const char *@S, ...

env.errx
	methodV,local,notoc
	fmt	const char *@S, ...

env.start
	method,local,notoc
	flags	u_int32_t @S

env.stat_clear
	method
	flags	u_int32_t @S

env.stat_print
	method
	stream	FILE *@S
	flags	u_int32_t @S

env.stop
	method,local,notoc
	flags	u_int32_t @S

env.toc_create
	method,local,notoc
	flags	u_int32_t @S
	tocp	WT_TOC **@S

###################################################
# Env getter/setter method declarations
###################################################
env.get_errcall
	method,getset
	errcall	void (**@S)(const ENV *, const char *)
env.set_errcall
	method,getset
	errcall	void (*@S)(const ENV *, const char *)

env.get_errfile
	method,getset
	errfile	FILE **@S
env.set_errfile
	method,getset
	errfile	FILE *@S

env.get_errpfx
	method,getset
	errpfx	const char **@S
env.set_errpfx
	method,getset
	errpfx	const char *@S

env.get_verbose
	method,getset
	verbose	u_int32_t *@S
env.set_verbose
	method,getset,verify
	verbose	u_int32_t @S

env.get_cachesize
	method,getset
	cachesize	u_int32_t *@S
env.set_cachesize
	method,getset
	cachesize	u_int32_t @S

###################################################
# WT_TOC method declarations
###################################################
wt_toc.destroy
	method,local,notoc
	flags	u_int32_t @S

###################################################
# Db standalone method declarations
###################################################
db.bulk_load
	method
	flags	u_int32_t @S
	cb	int (*@S)(DB *, DBT **, DBT **)

db.close
	method
	flags	u_int32_t @S

db.destroy
	method
	flags	u_int32_t @S

db.dump
	method,open
	stream	FILE *@S
	flags	u_int32_t @S

db.err
	methodV,local,notoc
	err	int @S
	fmt	const char *@S, ...

db.errx
	methodV,local,notoc
	fmt	const char *@S, ...

db.get
	method,local,open
	key	DBT *@S
	pkey	DBT *@S
	data	DBT *@S
	flags	u_int32_t @S

db.get_stoc
	method,open
	key	DBT *@S
	pkey	DBT *@S
	data	DBT *@S
	flags	u_int32_t @S

db.get_recno
	method,local,open
	recno	u_int64_t @S
	key	DBT *@S
	pkey	DBT *@S
	data	DBT *@S
	flags	u_int32_t @S

db.get_recno_stoc
	method,open
	recno	u_int64_t @S
	key	DBT *@S
	pkey	DBT *@S
	data	DBT *@S
	flags	u_int32_t @S

db.open
	method
	dbname	const char *@S
	mode	mode_t @S
	flags	u_int32_t @S

db.stat_clear
	method
	flags	u_int32_t @S

db.stat_print
	method
	stream	FILE * @S
	flags	u_int32_t @S

db.sync
	method,open
	flags	u_int32_t @S

db.verify
	method,open
	flags	u_int32_t @S

###################################################
# Db getter/setter method declarations
###################################################
db.get_errcall
	method,getset
	errcall	void (**@S)(const DB *, const char *)
db.set_errcall
	method,getset
	errcall	void (*@S)(const DB *, const char *)

db.get_errfile
	method,getset
	errfile	FILE **@S
db.set_errfile
	method,getset
	errfile	FILE *@S

db.get_errpfx
	method,getset
	errpfx	const char **@S
db.set_errpfx
	method,getset
	errpfx	const char *@S

db.get_btree_compare
	method,getset
	btree_compare	int (**@S)(DB *, const DBT *, const DBT *)
db.set_btree_compare
	method,getset
	btree_compare	int (*@S)(DB *, const DBT *, const DBT *)

db.get_btree_compare_int
	method,getset
	btree_compare_int	int *@S
db.set_btree_compare_int
	method,getset,verify
	btree_compare_int	int @S

db.get_btree_dup_compare
	method,getset
	btree_dup_compare	int (**@S)(DB *, const DBT *, const DBT *)
db.set_btree_dup_compare
	method,getset
	btree_dup_compare	int (*@S)(DB *, const DBT *, const DBT *)

db.get_btree_itemsize
	method,getset
	intlitemsize	u_int32_t *@S
	leafitemsize	u_int32_t *@S
db.set_btree_itemsize
	method,getset
	intlitemsize	u_int32_t @S
	leafitemsize	u_int32_t @S

db.get_btree_pagesize
	method,getset
	allocsize	u_int32_t *@S
	intlsize	u_int32_t *@S
	leafsize	u_int32_t *@S
	extsize	u_int32_t *@S
db.set_btree_pagesize
	method,getset
	allocsize	u_int32_t @S
	intlsize	u_int32_t @S
	leafsize	u_int32_t @S
	extsize	u_int32_t @S

db.get_btree_dup_offpage
	method,getset
	btree_dup_offpage	u_int32_t *@S
db.set_btree_dup_offpage
	method,getset
	btree_dup_offpage	u_int32_t @S
