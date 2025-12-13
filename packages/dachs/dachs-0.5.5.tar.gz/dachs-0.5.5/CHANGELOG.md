# CHANGELOG

## v0.5.5 (2025-12-08)

### Bug fixes

* **Project**: move dependencies to pyproject, tests deps to tox.ini ([`bc47e16`](https://github.com/BAMresearch/DACHS/commit/bc47e161313ac03e8c10b2d043f2b8f328ba9791))

### Continuous integration

* **Tests**: testing on Ubuntu & Windows ([`12c9554`](https://github.com/BAMresearch/DACHS/commit/12c95542676ccdbecf440bfdc161b0fb245cceb5))

* **Tests**: requirements file removed ([`c08f18e`](https://github.com/BAMresearch/DACHS/commit/c08f18e474a90f190fa610bde310dd73ceac5edc))

* **Cleanup**: remove templates and code now obsolete with updated copier config ([`16ed14f`](https://github.com/BAMresearch/DACHS/commit/16ed14f64f22386bd546181b78b1fccf8020f1e8))

* **Tests**: Run Github Action tests on Windows ([`8e9c76a`](https://github.com/BAMresearch/DACHS/commit/8e9c76ac94b5870dfc79bf20febd94a47e3b66e2))

## v0.5.4 (2025-12-08)

### Bug fixes

* **Project**: converted to copier project template, reapplied, updated ([`69d2476`](https://github.com/BAMresearch/DACHS/commit/69d24765ce1c1a57d647e41cb7d00c58523300cf))

* **McSAS3**: updated module names ([`6d26abf`](https://github.com/BAMresearch/DACHS/commit/6d26abf94b2ed2b9a001a40920fd2bc02a7d8efd))

### Testing

* **Notebook**: rerun for updated outputs ([`5f52fa5`](https://github.com/BAMresearch/DACHS/commit/5f52fa59bc43ee6e32aeb488d110008fa21fa39d))

### Unknown Scope

* Update authors list with Glen J. Smales ([`d50dae8`](https://github.com/BAMresearch/DACHS/commit/d50dae83de1074e08bf536ab84ed27e828db4560))

* Update LICENSE ([`b78d2de`](https://github.com/BAMresearch/DACHS/commit/b78d2de13bfcbc9d5c73e118eabfe0e31aee0e07))

* Update README.rst ([`363e850`](https://github.com/BAMresearch/DACHS/commit/363e850c17be8d9d9f4d75d240650dac6ab59ce8))

* Update README: link to internal doc pages ([`4a47042`](https://github.com/BAMresearch/DACHS/commit/4a47042b2469f9ead9b7c6d4a08fb4da6cf5c239))

* Added wash solvent, volume and number of washes ([`8f1f095`](https://github.com/BAMresearch/DACHS/commit/8f1f095e29cf217a8527fe467182b58751d7320e))

## v0.5.3 (2024-08-07)

### Bug fixes

* **Structure**: copy some parameters to DerivedParameters as well ([`b8833c6`](https://github.com/BAMresearch/DACHS/commit/b8833c6a26e6e308b2ccfa1ef3732eb466a7a6fb))

* **Structure**: increase note count with each note ([`c6547c7`](https://github.com/BAMresearch/DACHS/commit/c6547c77f34cfee013687a198ebfb16eca1840a9))

* **Reagent**: append component or reagent if not in list already ([`9067c63`](https://github.com/BAMresearch/DACHS/commit/9067c635c5234a0ccb547f7578f5485cb62fcb96))

### Continuous integration

* **docs**: install graphviz+dot on Windows ([`6c941d3`](https://github.com/BAMresearch/DACHS/commit/6c941d3910b9a4e8d760d78a5550e063c7bc643c))

* **docs**: install graphviz+dot on Windows ([`6eefd83`](https://github.com/BAMresearch/DACHS/commit/6eefd8363b7df390b92883dcc2aa026919c766f4))

* **coverage**: syntax fix ([`2b98edd`](https://github.com/BAMresearch/DACHS/commit/2b98eddccc55cad17f9952429cebe502e38f3f06))

### Documentation

* **Changelog**: updated ([`416bbdd`](https://github.com/BAMresearch/DACHS/commit/416bbddfcfb74cfe1ea0fcad795445eb97a173fa))

* **Structure**: adjust info messages/output ([`23f491b`](https://github.com/BAMresearch/DACHS/commit/23f491b58062a5c9acf1b4cf2fc7047cd57d3518))

* **notebook**: removed outputs for easier diff ([`5e70afb`](https://github.com/BAMresearch/DACHS/commit/5e70afb5f7901b7c79cd7774ae19a1bdab853198))

### Refactoring

* **structure**: make flake8 happy ([`2ede69c`](https://github.com/BAMresearch/DACHS/commit/2ede69cbb7b4c09021ab41868a7d531cf01738de))

### Testing

* **notebook**: added outputs again for testing ([`b57b2fe`](https://github.com/BAMresearch/DACHS/commit/b57b2fe40b4fd4894557993f3d97c3e774214a19))

* **requirements**: updated for chempy issues with numpy2 ([`98d1b57`](https://github.com/BAMresearch/DACHS/commit/98d1b576b232693b2d765ca04a91461b2dafa2cb))

* **Data**: adjusted test data ([`a4b0d1c`](https://github.com/BAMresearch/DACHS/commit/a4b0d1c44d427b22b58aa16911aa65c01801fe57))

### Unknown Scope

* previous update. ([`6393d38`](https://github.com/BAMresearch/DACHS/commit/6393d3805b17b89530abbda0cdce2defbbdacc02))

* Updated structure with more information ([`99a5206`](https://github.com/BAMresearch/DACHS/commit/99a520617e46d56e8323c3bac8503dda391514ec))

## v0.5.2 (2023-11-29)

### Bug fixes

* **structure**: logging to files ([`507fec6`](https://github.com/BAMresearch/DACHS/commit/507fec67e77b1d687204456d8cb1af44d65a76ca))

### Refactoring

* **Formatting**: black applied ([`b513bcc`](https://github.com/BAMresearch/DACHS/commit/b513bcc9c1eb378c7face9b1739195577e028b6f))

* **General**: removed unused import, isort'd ([`55ef37a`](https://github.com/BAMresearch/DACHS/commit/55ef37a97e656ae72ad88d574471018852a9228d))

### Testing

* **dachs**: tests need assertions ([`9e5eec4`](https://github.com/BAMresearch/DACHS/commit/9e5eec4c00f107ef087c243ba131d329577e0e00))

## v0.5.1 (2023-11-28)

### Bug fixes

* **notebook**: remove previously added locale change ([`016ed6b`](https://github.com/BAMresearch/DACHS/commit/016ed6b90a44f474aada68fab26bcd1600434270))

* **notebook**: ensure utf8 encoding (Windows) ([`0e950e1`](https://github.com/BAMresearch/DACHS/commit/0e950e19592b0da1603a3e110a2b6413a4c3af7f))

* **structure**: warn if syringe could not be parsed ([`9992fc2`](https://github.com/BAMresearch/DACHS/commit/9992fc2132fd21975df93e65dd3a73bc19d5fc52))

* **structure.create**: what if TotalLinkerMoles is not found? DivBy0 on L444 ([`8810462`](https://github.com/BAMresearch/DACHS/commit/8810462631bf43cf7a58c1f23283fc67aaadd931))

* **structure.create**: handle missing+optional Mixture container ([`d2d9cfa`](https://github.com/BAMresearch/DACHS/commit/d2d9cfaaa875d6abbd1e96e677326cd189bdf24e))

* **structure.create**: previousRLM might be empty ([`859b665`](https://github.com/BAMresearch/DACHS/commit/859b6654cb14d5b80038d9cfec8b49031b0dfa12))

* **find_in_log**: remove dummy exclude, make it empty list ([`5fe0cca`](https://github.com/BAMresearch/DACHS/commit/5fe0ccaa5c246f7acc6399db3b6cc1c3306dd5a6))

* **format**: syntax, put backslashes in raw string ([`747cde0`](https://github.com/BAMresearch/DACHS/commit/747cde03c8ca25eb75c350a7730772192e9b8bba))

* **reading**: handle optional columns gracefully (PriceDate, Using) ([`33a7897`](https://github.com/BAMresearch/DACHS/commit/33a7897b39af0273bf66b637e52aef831eca7656))

### Documentation

* **changelog**: fix commit message formatting ([`031ce53`](https://github.com/BAMresearch/DACHS/commit/031ce530df6020f9418d4f2a74372f1251d435b5))

* **changelog**: adjusted changelog for unreleased changes as well ([`21595ed`](https://github.com/BAMresearch/DACHS/commit/21595ed1e7d21e0a848df3b0c83bd07830af3fe1))

* **changelog**: modified changelog template, omit chore changes ([`8344ef6`](https://github.com/BAMresearch/DACHS/commit/8344ef615c8e1175e5b3f6ec5c903c7b4424a6bb))

* **changelog**: syntax fix ([`ecbad98`](https://github.com/BAMresearch/DACHS/commit/ecbad989817000af15afb4dfc01811433ded8669))

### Refactoring

* **General**: some extra print() disabled ([`37b1b31`](https://github.com/BAMresearch/DACHS/commit/37b1b313b44d182eb0aa73b9f14aa2990c12665e))

* **formatting**: comment ([`6223aa1`](https://github.com/BAMresearch/DACHS/commit/6223aa1a87c70ff1c1467f766c8aa4863cf6e321))

* **Naming**: consistent more specific name member, fixing tests ([`0d635d6`](https://github.com/BAMresearch/DACHS/commit/0d635d6967a6d6322dfa8b0c0b2e432668ae2ac2))

### Testing

* **notebook**: show .h5 files without full path which depends on platform ([`3e85944`](https://github.com/BAMresearch/DACHS/commit/3e859449e01014409112c0defe5f6d3f764402a3))

* **notebook**: show .h5 files found ([`0fb4d8e`](https://github.com/BAMresearch/DACHS/commit/0fb4d8e466f8aecf8dc8e44050058130f027f954))

* **dachs**: traceback info added, on failures ([`4060476`](https://github.com/BAMresearch/DACHS/commit/4060476f9a0a312a000092fe890f5968b948a0ce))

* **notebook**: ensure utf8 encoding, required for Windows ([`dc11f2a`](https://github.com/BAMresearch/DACHS/commit/dc11f2ac236051d5f652e9bc00a9fd91cdb2baa2))

* **notebook**: now with cell outputs ([`bddeb75`](https://github.com/BAMresearch/DACHS/commit/bddeb75de01c1c1f3947bb0ea6070ac1f7184656))

* **notebook**: updated for current structure ([`2426750`](https://github.com/BAMresearch/DACHS/commit/24267505447c00056afcf55dc39778b2824a91dc))

* **notebook**: remove notebook cell outputs ([`aa885f2`](https://github.com/BAMresearch/DACHS/commit/aa885f26d6497454a033a665ea65cce202b80531))

* **General**: updated file paths, output failing file names ([`bf0fc32`](https://github.com/BAMresearch/DACHS/commit/bf0fc3215919f8f2e9e043ee9e434deb310cff2e))

### Unknown Scope

* update test cases ([`0dff71a`](https://github.com/BAMresearch/DACHS/commit/0dff71a5ef0b24a2a55c662ff1889d05e9272c54))

* Adapting to support a third addditive ([`0ccce64`](https://github.com/BAMresearch/DACHS/commit/0ccce64120841cc0c1e2a8b9a74c342d5aeff8dd))

* improved data classes to offload work. ([`f13761e`](https://github.com/BAMresearch/DACHS/commit/f13761eb30c477d2096566dba1b86ac4b2eee691))

* Updating synthesis text generation ([`993136d`](https://github.com/BAMresearch/DACHS/commit/993136d6cac28e1d60ebf795771073f098aa7309))

* Updates on the text block and an additional yield ([`cc2931e`](https://github.com/BAMresearch/DACHS/commit/cc2931e7776ae59fd84015a3e6c94aaae45a2bf3))

* naming improvements, synthesis text generation ([`207a6e1`](https://github.com/BAMresearch/DACHS/commit/207a6e1edd358358a74574ecbc70f65922afe1b3))

* fixing time, yield calc issues, improving naming ([`c678f54`](https://github.com/BAMresearch/DACHS/commit/c678f54e35aa0973f8d68539bc64894f247921b2))

* small upgrade to reaction times ([`ed1aba0`](https://github.com/BAMresearch/DACHS/commit/ed1aba0b85f4b1c7daa192fda1bc29b5bce656fd))

* small update ([`a34592f`](https://github.com/BAMresearch/DACHS/commit/a34592f31d31361c6ab9f8d40f0a59dae0de1ced))

* Replaced KeyParameters w/more detailed DerivedPara ([`c7ba0a6`](https://github.com/BAMresearch/DACHS/commit/c7ba0a6495ff94f4ad276acd62febdfb35f66b39))

* Result of bug-squashing event with Glen ([`5173ca7`](https://github.com/BAMresearch/DACHS/commit/5173ca73577d9286c292990403a148153228445c))

* Adding support for density of mixtures. ([`de695fe`](https://github.com/BAMresearch/DACHS/commit/de695feb210f1a34fef56d3f76db527241083788))

* find_in_log will never return None, clarified. ([`f5d83a3`](https://github.com/BAMresearch/DACHS/commit/f5d83a3f68f8460b0e3fe2ebd849c792290292e7))

* removed SynthesisLog-type messages -> RawLog ([`e0486f1`](https://github.com/BAMresearch/DACHS/commit/e0486f1137a0baeaa835d4b52873ef78acd714fd))

* adding ProductYield to ExtraInformation ([`0df24b1`](https://github.com/BAMresearch/DACHS/commit/0df24b187bad49257cb1be3386df38b9d528defd))

* skipping blank lines in logs ([`40f8114`](https://github.com/BAMresearch/DACHS/commit/40f81142927934640231b62e912fbc865ab66dd5))

* Adding "Using" to the RawLogMessages ([`95e2552`](https://github.com/BAMresearch/DACHS/commit/95e25520ec3499c749be04aa2571d943c5802d08))

* helper function to split a rowan log per sample. ([`46d0df1`](https://github.com/BAMresearch/DACHS/commit/46d0df13c137f79f92889b6be3409d900eaf70aa))

* Removing final mentions of "weight" and minor fix ([`3de5078`](https://github.com/BAMresearch/DACHS/commit/3de5078bf39b7a0c8bfd526f5b2b6db30ec85f11))

## v0.5.0 (2023-07-28)

### Bug fixes

* **Notebook**: adjusted for Dash 2.11, tests successful here ([`31ab924`](https://github.com/BAMresearch/DACHS/commit/31ab924e94f32cf1c2ef9bad6a1d87f48b457d9a))

* **helpers.whitespaceCleanup**: handle Series object properly ([`f5e791e`](https://github.com/BAMresearch/DACHS/commit/f5e791e6a858969bf7d11b856b5abd9282b71f06))

* **serialization**: dumpKV() omits custom dachs types now but stores type info ([`cdbbbcc`](https://github.com/BAMresearch/DACHS/commit/cdbbbcc3a10e9bd036ca3dfdd355654f9ba6c735))

* **Equipment.Description**: filter out NaN (set to '') values while parsing ([`2da1957`](https://github.com/BAMresearch/DACHS/commit/2da1957ceb8944a2a4c1e9cd63ebc7ba8c76e733))

* **serialization.graphKV**: fixed for node names containing colons ':' ([`8570cbb`](https://github.com/BAMresearch/DACHS/commit/8570cbbf802ed12d5bc94fe5670eff2ab97d2d6f))

* **equipment.PV**: reader/parser fixed for extended LogBook xslx format ([`5cfd521`](https://github.com/BAMresearch/DACHS/commit/5cfd521d5196c8d6bb008f4fe7f13859975fe9c1))

### Features

* **equipment.PV**: updated converters and validators ([`85ed382`](https://github.com/BAMresearch/DACHS/commit/85ed382c5c7559e38d918b4df5493e8201fcd12e))

* **Physical Values**: parsing PVs from Logbook .xlsx file to PVs and storing them to HDF5 ([`9403b40`](https://github.com/BAMresearch/DACHS/commit/9403b40f6a65f1ecae426eb5002e004c78dfc17f))

### Refactoring

* **serialization**: removed obsolete filterStoragePaths() ([`5eee1fb`](https://github.com/BAMresearch/DACHS/commit/5eee1fb899c39c3b3ab22f876022517c75eaebc8))

* **serialization**: debug output improved ([`850b293`](https://github.com/BAMresearch/DACHS/commit/850b2939b54bab5ba44f5113868cf9aa24ea129d))

* **main**: file mode change ([`795d93b`](https://github.com/BAMresearch/DACHS/commit/795d93b860ab15dcb446c1cf31085d5a336a8a38))

* **General**: regular python files shall not have executable bit set ([`b3635f4`](https://github.com/BAMresearch/DACHS/commit/b3635f4d983a8e10bc6b4ee18376fc33a187e19b))

* **PV**: class names shall be in TitleCase ([`13e9304`](https://github.com/BAMresearch/DACHS/commit/13e9304a05dcbdd802908b0090c2a25166638c28))

### Testing

* **requirements**: fixed chempy version to prevent KeyError about . in formula ([`6126f4e`](https://github.com/BAMresearch/DACHS/commit/6126f4eb6d9db960b9c099643ad9a74b0eadb999))

* **PV**: fixed tests for recent PV changes ([`ca51989`](https://github.com/BAMresearch/DACHS/commit/ca519892d82e65e691ab3778cf012ec4d96829e7))

### Unknown Scope

* Updated Logbook with actual PVs and extra info ([`b0bafab`](https://github.com/BAMresearch/DACHS/commit/b0bafabdd40118de48019cdf04e4ba62e7fc09a6))

## v0.4.3-dev.5 (2023-06-09)

### Refactoring

* **main**: separate main.py for code to be reused in tests ([`d62f195`](https://github.com/BAMresearch/DACHS/commit/d62f19530decca1cb9d0dc8b76348def58db8ad0))

* **scripts**: RunMultiple.sh updated for path handling ([`2eb6b01`](https://github.com/BAMresearch/DACHS/commit/2eb6b0125dbe66c3a72e99f96e11592659a28b6d))

* **formatting**: some fixes to agree with flake8 and isort, some reformatting by black ([`f614cb1`](https://github.com/BAMresearch/DACHS/commit/f614cb176415dcb683f2e3a366b7bfdc2ae9ff6b))

### Testing

* **structure**: prevent pytest args to slip through to argparse ([`17039b3`](https://github.com/BAMresearch/DACHS/commit/17039b3ff02c1cc414558e1217ac0fe3f65a9d75))

* **notebook**: note on source .h5 files, outputs for .h5 files generated by tests earlier ([`27c3f7b`](https://github.com/BAMresearch/DACHS/commit/27c3f7b1318c410050bf315606f6806d72a02981))

* **structure**: using code from main to generate .h5 files, more dependencies ([`395b2ca`](https://github.com/BAMresearch/DACHS/commit/395b2cae8044b6091d49b7177c44d624cb3d00e3))

## v0.4.3-dev.3 (2023-06-02)

### Testing

* **Pint**: fix currency units definition for latest Pint 0.22 ([`315222a`](https://github.com/BAMresearch/DACHS/commit/315222aae933d1242ca29a777536c3f57c306a17))

* **reagent**: fix PreparationDate argument ([`6bdeba5`](https://github.com/BAMresearch/DACHS/commit/6bdeba5d597926e9346226a0f13e125622e1a6be))

## v0.4.3-dev.2 (2023-05-04)

### Code style

* **readers**: trailing whitespace (W291) removed ([`441a4c4`](https://github.com/BAMresearch/DACHS/commit/441a4c4fb65b9844d9436b095c642046c4a35409))

## v0.4.3-dev.1 (2023-05-04)

### Code style

* **structure**: black formatter ([`81f160f`](https://github.com/BAMresearch/DACHS/commit/81f160f875bdf0295a23aa2c7c99fd6f98552bbf))

### Unknown Scope

* Computation of solution age added to extraInfo ([`df5dd85`](https://github.com/BAMresearch/DACHS/commit/df5dd859e0194f086018a030334890ca2e4e37e5))

* added test case for AutoMOF_6 series ([`4fa9ec3`](https://github.com/BAMresearch/DACHS/commit/4fa9ec3ede82b8004abe6aac275a737895ff887d))

* preparing for AutoMOF 6&7 ([`1d53806`](https://github.com/BAMresearch/DACHS/commit/1d5380676c3679e4248b678183065f217cd2188e))

* Shell script to run AutoMOF05 ([`755431d`](https://github.com/BAMresearch/DACHS/commit/755431d90364df1cbfce1784aefd468e7650b25b))

* script to pick apart the raw logs from RoWan ([`5918e0d`](https://github.com/BAMresearch/DACHS/commit/5918e0dacaaadf0ac4921f26b1a8e2a6a894730b))

* Readin example jupyter notebook launching Dash ([`afa6065`](https://github.com/BAMresearch/DACHS/commit/afa60659c206e583918d6ec1f8e1143d5734abc4))

* making a read-in structure python notebook ([`09a1e55`](https://github.com/BAMresearch/DACHS/commit/09a1e550aa0cca0acfdd0bcdacb02f9af10ae908))

* tests(structure): set AMSET in tests to succeed ([`e7740a5`](https://github.com/BAMresearch/DACHS/commit/e7740a5dbf703ba20c1b931de9e41a4398be79cf))

* removing superfluous weight determination ([`5ff5fd9`](https://github.com/BAMresearch/DACHS/commit/5ff5fd99e5792818bf39c7136ea6bad0397b6f95))

* reimplementing calibration and CLI AMSET option ([`9a4c70f`](https://github.com/BAMresearch/DACHS/commit/9a4c70f8bbfb5fe53331188518e324068f91b6ff))

## v0.4.2 (2023-04-20)

### Bug fixes

* **serialization**: Graph SVG with transparent background ([`366287c`](https://github.com/BAMresearch/DACHS/commit/366287c12109ded89c39dc91519c9e955ed27806))

### Documentation

* **general**: logo ([`febf8f0`](https://github.com/BAMresearch/DACHS/commit/febf8f04f9d5bf59652e3dcba269659e85d6f40a))

## v0.4.1 (2023-04-18)

### Bug fixes

* **GitHub Actions**: Make new release only if tests succeed ([`94f7a25`](https://github.com/BAMresearch/DACHS/commit/94f7a25b9bb0021b27b267d7e717921d015a185a))

* **requirements**: graphviz added for tests ([`a06f87d`](https://github.com/BAMresearch/DACHS/commit/a06f87de270810c613f822c3168b409fba201e78))

## v0.4.0 (2023-04-17)

### Bug fixes

* **data import**: whitespace cleanup for texts/descriptions ([`005be00`](https://github.com/BAMresearch/DACHS/commit/005be006aed3f8055db566804e0ac71e0a9f7226))

* **ExperimentalSetupClass**: removing redundant whitespace from description ([`5429102`](https://github.com/BAMresearch/DACHS/commit/542910217cd0c5bf1b1e96ac919a00739aa6ccce))

* **readers**: unwanted DataFrame string formatting ([`880ca0d`](https://github.com/BAMresearch/DACHS/commit/880ca0d1195f90cd244ef05189019149a314785b))

### Documentation

* **visualization**: Generate SVG Graph in __main__ ([`31f38f9`](https://github.com/BAMresearch/DACHS/commit/31f38f9fbea9fd16d87a65f7c908253a970d5f8c))

* **visualization**: Graph building code added, WIP ([`1e1ffed`](https://github.com/BAMresearch/DACHS/commit/1e1ffed5c129ba8d6299fbf2bf0148b2ab4afd08))

### Features

* **serialization**: use the ID for path prefix at singular objects as well ([`60a08eb`](https://github.com/BAMresearch/DACHS/commit/60a08eb256f6a920d0e7e047025fa28418029e29))

### Refactoring

* **ExperimentalSetupClass**: comment about intended behaviour ([`9a41f7b`](https://github.com/BAMresearch/DACHS/commit/9a41f7be0e57cf94f506e354c91f95acc2392ff7))

## v0.3.0 (2023-04-05)

### Bug fixes

* **command line**: typo in usage texts ([`cf39d14`](https://github.com/BAMresearch/DACHS/commit/cf39d142785de9b0c767dfa5d83f1eed019c61cd))

### Documentation

* **structure**: fix format ([`4ccaf91`](https://github.com/BAMresearch/DACHS/commit/4ccaf91e6bd81e263ca4b438e4a76d2573868046))

* **readme**: notes on command line usage ([`4d11686`](https://github.com/BAMresearch/DACHS/commit/4d11686b0921027590e370c64ffad94c9699599a))

### Features

* **command line**: new parameter -o allows to specify location and name of HDF5 output file ([`fab741a`](https://github.com/BAMresearch/DACHS/commit/fab741a09d924e59d24f53d5375c62b9dc758e2d))

### Refactoring

* **serialization**: use McHDF.storeKVPairs avoids separate loop ([`34b9cd9`](https://github.com/BAMresearch/DACHS/commit/34b9cd93aaf6a490ec24c2b2f88d510994c9b988))

* **serialization**: add type info ([`1e946d4`](https://github.com/BAMresearch/DACHS/commit/1e946d4ef2eb49c26fe465dd8d2a09bfbb6ae613))

* **serialization**: rename storagePaths() -> dumpKV() ([`4ac7f96`](https://github.com/BAMresearch/DACHS/commit/4ac7f960cc7a9a1ffaa81d12fc2f4e505e0b2d79))

* **structure**: main module reuses structure.create() ([`be72352`](https://github.com/BAMresearch/DACHS/commit/be723521685146a827e1d3b6dc59b83b07fd966c))

* **structure**: moved testing code to separate module for reuse ([`6b78abf`](https://github.com/BAMresearch/DACHS/commit/6b78abf927af108a02f6b080b6730575aaffcfdd))

* **root**: rename top-level class to more meaningful name *Experiment* ([`0fe03dc`](https://github.com/BAMresearch/DACHS/commit/0fe03dcc86a4ce08e7d1e8608792bb76fd27a426))

## v0.2.0 (2023-04-04)

### Code style

* **serialization**: fix file header ([`029c20c`](https://github.com/BAMresearch/DACHS/commit/029c20c94823a30c92b20b468b1db5fd78cb8ebd))

### Documentation

* **readme**: info & reminder how to get stdout/stderr with pytest ([`20fc960`](https://github.com/BAMresearch/DACHS/commit/20fc9601a9675882fdc4119349291f2c2a6a1fb6))

### Features

* **ComponentMasses**: store as dict associated to their respective Component ([`a797b0b`](https://github.com/BAMresearch/DACHS/commit/a797b0b61bbd754eed46d80b1aafdc63d5898b0f))

* **serialization**: use object IDs instead of numerical index where available ([`fef04b0`](https://github.com/BAMresearch/DACHS/commit/fef04b051529510867843ab1721398acced6d3ce))

### Unknown Scope

* tests(structure): commented core for dumping all storage paths ([`450d660`](https://github.com/BAMresearch/DACHS/commit/450d66084076d13b27028fbf5e328f86ce89be1a))

## v0.1.2 (2023-04-03)

### Bug fixes

* **Serialization**: store lists of quantities, fixes #7 ([`d311d5b`](https://github.com/BAMresearch/DACHS/commit/d311d5bd075cb5c9c465819301b5fb8d38652eaf))

* **EquipmentList**: price unit parsing ([`971a54d`](https://github.com/BAMresearch/DACHS/commit/971a54d6b98e47e27b55520604f356f83d05f525))

### Refactoring

* **Tests**: mcsas3 can be installed with pip now ([`4d17768`](https://github.com/BAMresearch/DACHS/commit/4d177680192e04ca0a9dcfba8ed339f22dc9008f))

## v0.1.2-dev.3 (2023-03-31)

### Code style

* **documentation**: comment formatting ([`1129c56`](https://github.com/BAMresearch/DACHS/commit/1129c56faf7ce26fabdc43f3f113a269ca54e8b8))

## v0.1.2-dev.2 (2023-03-31)

### Code style

* **changelog**: version number prefixed by v ([`1840736`](https://github.com/BAMresearch/DACHS/commit/18407365ab6927c52d4fdecdf256ffc0f6c46c51))

### Documentation

* **General**: inheritance diagram in reference ([`946cdd8`](https://github.com/BAMresearch/DACHS/commit/946cdd838430b619c4fe9bee53039774b17ef98e))

## v0.1.1 (2023-03-28)

### Bug fixes

* **reagent**: adjust units and method names for tests to succeed ([`0b5b21e`](https://github.com/BAMresearch/DACHS/commit/0b5b21eb4985955f03629e385b979244e4f0a3e0))

### Code style

* **general**: satisfy flake8 ([`ce44d64`](https://github.com/BAMresearch/DACHS/commit/ce44d649c5c3653a08d646b749b7f2c4bb3af68c))

* **general**: code formatting line length set to 115 ([`d013773`](https://github.com/BAMresearch/DACHS/commit/d01377318944d72a0a5911e933be4f42eb80a725))

* **general**: reformat main.py, whitespace fixes ([`7b9954b`](https://github.com/BAMresearch/DACHS/commit/7b9954b47594a953459e23042b518386916020f1))

* **general**: isort imports ([`0467ca3`](https://github.com/BAMresearch/DACHS/commit/0467ca37972cf42e328e280ce4b97338e3e99e15))

* **general**: formatted with black ([`1b67618`](https://github.com/BAMresearch/DACHS/commit/1b6761825cb0b2b8d0b800c25e8ce36d9b772611))

* **line length**: 115) ([`4b19763`](https://github.com/BAMresearch/DACHS/commit/4b19763770de89ea4edc10d4cfd923399b02823a))

### Documentation

* **general**: disable link check temporarily ([`332a112`](https://github.com/BAMresearch/DACHS/commit/332a112064f4727461a7e2dd3b4de4cd829bf0d3))

* **general**: remove section title ([`d1fd17b`](https://github.com/BAMresearch/DACHS/commit/d1fd17b119e2765e014e6f929b0cfccd1061a1b3))

* **general**: initial setup ([`a490cb1`](https://github.com/BAMresearch/DACHS/commit/a490cb1fb7210160eb52ae428de22b340ffb389d))

* **project**: readme updated ([`caed30c`](https://github.com/BAMresearch/DACHS/commit/caed30c33f9528cc7471fabca92d0e01549ea4a3))

### Refactoring

* **general**: fix ureg imports ([`38e7a19`](https://github.com/BAMresearch/DACHS/commit/38e7a1926bd94bf37d31ff26ec5528ed0dc339ef))

### Unknown Scope

* v0.1.0 ([`e9e288f`](https://github.com/BAMresearch/DACHS/commit/e9e288f0ffe678e5a65ad825167888f8c1b7c845))

* Many small fixes, now also runs from CLI ([`a06bb98`](https://github.com/BAMresearch/DACHS/commit/a06bb98aadccb77f5146684e5c40b761398e0cd7))

* adding yield, ML ratio, more test cases ([`3fe80a9`](https://github.com/BAMresearch/DACHS/commit/3fe80a9b5ebfd0a842c9fe6772734ede885a578f))

* Fix for the DACHS paths issue and other minor ([`6dc1362`](https://github.com/BAMresearch/DACHS/commit/6dc1362117f9b8f1fa33b6faaf973e062842c539))

* added the reaction mixture and automatic mm calcs. ([`36a90df`](https://github.com/BAMresearch/DACHS/commit/36a90df5d1b97b0735d133698ef7da42632561b4))

* tests passing ([`9aa39ef`](https://github.com/BAMresearch/DACHS/commit/9aa39ef97ab85710f1709c5930b51d72aa83e882))

* Mixture class operational, structure test broken. ([`e5d8e7e`](https://github.com/BAMresearch/DACHS/commit/e5d8e7e953442abe59cf736ebf093fbca9890861))

* Updated naming and start on Mixture class. ([`6846636`](https://github.com/BAMresearch/DACHS/commit/68466365c508b92a91e96b96673859e145be3b16))

* adjusting reagent, but will rewrite mixture ([`44f9108`](https://github.com/BAMresearch/DACHS/commit/44f910817aeda882046b18dcefaf5161f5867081))

* Provisioning some essential derived data on mixes ([`f657f79`](https://github.com/BAMresearch/DACHS/commit/f657f79cb9e9ad25d54e05f36ad50235f83543a7))

* added price per volume and mass to reagent ([`a084f21`](https://github.com/BAMresearch/DACHS/commit/a084f21a8305cc81f88a7b97bfc8cfff22ee8e67))

* bugfixes ([`976b687`](https://github.com/BAMresearch/DACHS/commit/976b687297f60d8c009a570492b5a118e7c09301))

* equipment and experimentalSetup unit test ([`2750dcd`](https://github.com/BAMresearch/DACHS/commit/2750dcdec472c432c2ff2abea42314d130fee062))

* Changed UID to ID and fixed excel read ([`a1ccde0`](https://github.com/BAMresearch/DACHS/commit/a1ccde0d1d325fa5d441e7e09579df99d53953d5))

* using updated McHDF.storeKV() ([`e7fa4de`](https://github.com/BAMresearch/DACHS/commit/e7fa4ded170c1d42a796397d4ac3c3df283a6a2a))

* disabled debug output ([`4621d21`](https://github.com/BAMresearch/DACHS/commit/4621d21a8296c1fbe15fc4178174d2d2905daaf7))

* using PurePath for hdf5 path, to work in Windows as well ([`3c2f4d3`](https://github.com/BAMresearch/DACHS/commit/3c2f4d34ed784522e9743de1f6484d80b424ee25))

* using PurePosixPath for hdf5 path not being filesystem related ([`d9caa87`](https://github.com/BAMresearch/DACHS/commit/d9caa8701cc5cac2d86ceca092b34bf2a7839821))

* remove defaults for required fields ([`90487d5`](https://github.com/BAMresearch/DACHS/commit/90487d5ef995a3ab489a1d975bbc7265caec0c8d))

* hdf5 export in test_integral() using McSAS3 writer ([`4b627d8`](https://github.com/BAMresearch/DACHS/commit/4b627d8ba920c66c9864514f79571c8711d9eea6))

* fixed test_integral() ([`22257c7`](https://github.com/BAMresearch/DACHS/commit/22257c72d93df9c0299e6959dd69a3e6efbd6972))

* removed empty file ([`eb4ad06`](https://github.com/BAMresearch/DACHS/commit/eb4ad069ed15cab926dc38bbbfd876baf612391c))

* Adding derived parameters extractors, not yet work ([`90dcf7f`](https://github.com/BAMresearch/DACHS/commit/90dcf7f451b42fdde17a47212f6cc02c1e626a1e))

* Modified support for derived parameters ([`404a746`](https://github.com/BAMresearch/DACHS/commit/404a746801afebc270034ec73eaaa89f0d567dda))

* Added readers for message log and starting compoun ([`b04479f`](https://github.com/BAMresearch/DACHS/commit/b04479f972aa98c06b51116f118267cb951d7ff1))

* Added RawLogMessage tests ([`0343aeb`](https://github.com/BAMresearch/DACHS/commit/0343aeb0ef2581bc80be23db4293b9b970a83950))

* Created and moved pytests to tests directory ([`24541c2`](https://github.com/BAMresearch/DACHS/commit/24541c25938e69a599c173d9df25ced7411a2158))

* file name typo ([`e1c09cf`](https://github.com/BAMresearch/DACHS/commit/e1c09cf74ba28109284e00c4d7d5832ba8c0d82f))

* let git ignore macOS file meta data ([`cfc8642`](https://github.com/BAMresearch/DACHS/commit/cfc86423166f1745c347fd0e076e5105721574bd))

* Change datacass factory for optionals. test update ([`05ab72d`](https://github.com/BAMresearch/DACHS/commit/05ab72d2c54fcbb77211cf390d51e5b86af84c5c))

* small modifications to get the test working ([`70ba6d1`](https://github.com/BAMresearch/DACHS/commit/70ba6d1ffb9fa497dcb010a4371267e0cb2b55b5))

* packaging and versioneer. ([`7acd484`](https://github.com/BAMresearch/DACHS/commit/7acd4846d6520e14d5653a4d4b904e5dca356444))

* support for concentration calculations in mixture ([`c4ff11b`](https://github.com/BAMresearch/DACHS/commit/c4ff11b42859fd874ab886e9445daaaa5b66311e))

* Updates. Can now do mixtures of reagents ([`0ed07a6`](https://github.com/BAMresearch/DACHS/commit/0ed07a6db4b43a10bb9fbaafd2a3dc3853d3a6e0))

* probably better with raw strings. ([`327ba00`](https://github.com/BAMresearch/DACHS/commit/327ba00289dcc874105fb802a84cc72a08522200))

* addition of a UID, for storing in HDF5 tree ([`8783109`](https://github.com/BAMresearch/DACHS/commit/8783109e3921e27d7f02b41fac820db5c75a3afc))

* unit and unit conversions added. ([`0557be3`](https://github.com/BAMresearch/DACHS/commit/0557be33e817e7a183b1894b4de73c4d2969f19e))

* Added units support, see MolarMass ([`16ee937`](https://github.com/BAMresearch/DACHS/commit/16ee9371644f6ea4ab8e33aa323588ace87ee440))

* reagent now has a convenient items() iterable ([`8c1914b`](https://github.com/BAMresearch/DACHS/commit/8c1914b65339a1793a99a06975dd97388ca11f6e))

* Reagent class, just as example ([`331be46`](https://github.com/BAMresearch/DACHS/commit/331be460b0305de7028af7b4fa1306a53303dcd1))

* Initial commit ([`b0a911d`](https://github.com/BAMresearch/DACHS/commit/b0a911d43c697a2d9d6b9cdbde97ea0e76d57604))
