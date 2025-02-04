DROP TABLE IF EXISTS "mech_data";

CREATE TABLE "mech_data" (
    "mech_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "group_name" TEXT,
    "mech_class" TEXT,
    "variant" TEXT,
    "tonnage" INTEGER,
    "technology" TEXT,
    "cost" INTEGER,
    "rules" TEXT,
    "tro_id" INTEGER,
    "tro" TEXT,
    "rs_id" INTEGER,
    "rs" TEXT,
    "era_icon" TEXT,
    "date_introduced" TEXT,
    "era_id" INTEGER,
    "era_start" INTEGER,
    "image_url" TEXT,
    "is_featured" INTEGER,
    "is_published" INTEGER,
    "release" NUMERIC,
    "type" TEXT,
    "role" TEXT,
    "battle_value" INTEGER,
    "bf_type" TEXT,
    "bf_size" INTEGER,
    "bf_move" TEXT,
    "bf_tmm" INTEGER,
    "bf_armor" INTEGER,
    "bf_structure" INTEGER,
    "bf_threshold" INTEGER,
    "bf_damage_short" INTEGER,
    "bf_damage_short_min" INTEGER,
    "bf_damage_medium" INTEGER,
    "bf_damage_medium_min" INTEGER,
    "bf_damage_long" INTEGER,
    "bf_damage_long_min" INTEGER,
    "bf_damage_extreme" INTEGER,
    "bf_damage_extreme_min" INTEGER,
    "bf_overheat" INTEGER,
    "bf_point_value" INTEGER,
    "bf_abilities" TEXT,
    "skill" INTEGER,
    "formated_tonnage" TEXT,
    "armor" TEXT,
    "base_chassis_heat_sinks" INTEGER,
    "capabilities" TEXT,
    "capability" TEXT,
    "center_leg" BLOB,
    "center_torso" BLOB,
    "cl_armor" INTEGER,
    "cockpit" TEXT,
    "config" TEXT,
    "ct_armor" INTEGER,
    "ct_armor_type" TEXT,
    "deployment" TEXT,
    "ejection" TEXT,
    "engine" TEXT,
    "era" INTEGER,
    "fll_armor" INTEGER,
    "frl_armor" INTEGER,
    "front_left_leg" BLOB,
    "front_right_leg" BLOB,
    "gyro" TEXT,
    "hd_armor" INTEGER,
    "hd_armor_type" TEXT,
    "head" BLOB,
    "heat_sinks" TEXT,
    "hist" TEXT,
    "history" TEXT,
    "image_file" TEXT,
    "image" BLOB,
    "jump_mp" INTEGER,
    "la_armor" INTEGER,
    "la_armor_type" TEXT,
    "lam" TEXT,
    "left_arm" BLOB,
    "left_leg" BLOB,
    "left_torso" BLOB,
    "ll_armor" INTEGER,
    "ll_armor_type" TEXT,
    "lt_armor" INTEGER,
    "lt_armor_type" TEXT,
    "manufacturer" TEXT,
    "mass" INTEGER,
    "mech_name" TEXT,
    "motive" TEXT,
    "myomer" TEXT,
    "nocrit" TEXT,
    "notes" TEXT,
    "overview" TEXT,
    "primary_factory" TEXT,
    "ra_armor" INTEGER,
    "ra_armor_type" TEXT,
    "rear_left_leg" BLOB,
    "rear_right_leg" BLOB,
    "right_arm" BLOB,
    "right_leg" BLOB,
    "right_torso" BLOB,
    "rl_armor" INTEGER,
    "rl_armor_type" TEXT,
    "rll_armor" INTEGER,
    "rrl_armor" INTEGER,
    "rt_armor" INTEGER,
    "rt_armor_type" TEXT,
    "rtc_armor" INTEGER,
    "rtl_armor" INTEGER,
    "rtr_armor" INTEGER,
    "rules_level" INTEGER,
    "source" TEXT,
    "structure" TEXT,
    "system_manufacturer" BLOB,
    "system_mode" BLOB,
    "tech_base" TEXT,
    "version" TEXT,
    "walk_mp" INTEGER,
    "weapons" BLOB
)