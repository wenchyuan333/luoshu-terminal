(* WChyuanLuoShu.wl *)
(* LSHU-F3-RARE-001 executable reproducer *)
(* Miya diagnostic-repaired version, 2026-08-28 *)
(* Notion SSOT: LSHU-F3-RARE-001 + ARTIFACT WCHYUAN-LUOSHU-WL-001 *)

BeginPackage["WChyuanLuoShu`"];

CountLuoShu::usage =
  "CountLuoShu[d] counts d×d matrices over F_3 with all entries in {1,2} that are invertible over F_3.";

GLOrder::usage =
  "GLOrder[d, p:3] returns |GL(d, F_p)|.";

LuoShuRarity::usage =
  "LuoShuRarity[d] returns N(d)/|GL(d, F_3)|.";

CountLuoShu[d_Integer?Positive] := Module[
  {allElts, invertible},
  allElts = Tuples[{1, 2}, {d, d}];
  invertible = Select[allElts, Mod[Det[#], 3] =!= 0 &];
  Length[invertible]
];

GLOrder[d_Integer?Positive, p_: 3] :=
  Product[p^d - p^k, {k, 0, d - 1}];

LuoShuRarity[d_Integer?Positive] :=
  N[CountLuoShu[d] / GLOrder[d]];

EndPackage[];

(* Self-tests — expected outputs *)
(* Expected: CountLuoShu[3] == 192 *)
(* Expected: GLOrder[3] == 11232 *)
(* Expected: LuoShuRarity[3] ≈ 0.01709 (i.e. 1.7094%) *)

Print["CountLuoShu[3] = ", CountLuoShu[3], "  (expect 192)"];
Print["GLOrder[3]     = ", GLOrder[3], "  (expect 11232)"];
Print["Rarity(3)      = ", LuoShuRarity[3]*100, " %  (expect ≈1.7094%)"];
