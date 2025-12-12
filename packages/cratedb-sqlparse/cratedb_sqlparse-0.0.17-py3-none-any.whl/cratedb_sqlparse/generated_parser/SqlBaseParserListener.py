# Generated from SqlBaseParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SqlBaseParser import SqlBaseParser
else:
    from SqlBaseParser import SqlBaseParser

# This class defines a complete listener for a parse tree produced by SqlBaseParser.
class SqlBaseParserListener(ParseTreeListener):

    # Enter a parse tree produced by SqlBaseParser#statements.
    def enterStatements(self, ctx:SqlBaseParser.StatementsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#statements.
    def exitStatements(self, ctx:SqlBaseParser.StatementsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleStatement.
    def enterSingleStatement(self, ctx:SqlBaseParser.SingleStatementContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleStatement.
    def exitSingleStatement(self, ctx:SqlBaseParser.SingleStatementContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#singleExpression.
    def enterSingleExpression(self, ctx:SqlBaseParser.SingleExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#singleExpression.
    def exitSingleExpression(self, ctx:SqlBaseParser.SingleExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#default.
    def enterDefault(self, ctx:SqlBaseParser.DefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#default.
    def exitDefault(self, ctx:SqlBaseParser.DefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#begin.
    def enterBegin(self, ctx:SqlBaseParser.BeginContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#begin.
    def exitBegin(self, ctx:SqlBaseParser.BeginContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#startTransaction.
    def enterStartTransaction(self, ctx:SqlBaseParser.StartTransactionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#startTransaction.
    def exitStartTransaction(self, ctx:SqlBaseParser.StartTransactionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#commit.
    def enterCommit(self, ctx:SqlBaseParser.CommitContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#commit.
    def exitCommit(self, ctx:SqlBaseParser.CommitContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#explain.
    def enterExplain(self, ctx:SqlBaseParser.ExplainContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#explain.
    def exitExplain(self, ctx:SqlBaseParser.ExplainContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#optimize.
    def enterOptimize(self, ctx:SqlBaseParser.OptimizeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#optimize.
    def exitOptimize(self, ctx:SqlBaseParser.OptimizeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#refreshTable.
    def enterRefreshTable(self, ctx:SqlBaseParser.RefreshTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#refreshTable.
    def exitRefreshTable(self, ctx:SqlBaseParser.RefreshTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#update.
    def enterUpdate(self, ctx:SqlBaseParser.UpdateContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#update.
    def exitUpdate(self, ctx:SqlBaseParser.UpdateContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#delete.
    def enterDelete(self, ctx:SqlBaseParser.DeleteContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#delete.
    def exitDelete(self, ctx:SqlBaseParser.DeleteContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#showTransaction.
    def enterShowTransaction(self, ctx:SqlBaseParser.ShowTransactionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#showTransaction.
    def exitShowTransaction(self, ctx:SqlBaseParser.ShowTransactionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#showCreateTable.
    def enterShowCreateTable(self, ctx:SqlBaseParser.ShowCreateTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#showCreateTable.
    def exitShowCreateTable(self, ctx:SqlBaseParser.ShowCreateTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#showTables.
    def enterShowTables(self, ctx:SqlBaseParser.ShowTablesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#showTables.
    def exitShowTables(self, ctx:SqlBaseParser.ShowTablesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#showSchemas.
    def enterShowSchemas(self, ctx:SqlBaseParser.ShowSchemasContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#showSchemas.
    def exitShowSchemas(self, ctx:SqlBaseParser.ShowSchemasContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#showColumns.
    def enterShowColumns(self, ctx:SqlBaseParser.ShowColumnsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#showColumns.
    def exitShowColumns(self, ctx:SqlBaseParser.ShowColumnsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#showSessionParameter.
    def enterShowSessionParameter(self, ctx:SqlBaseParser.ShowSessionParameterContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#showSessionParameter.
    def exitShowSessionParameter(self, ctx:SqlBaseParser.ShowSessionParameterContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alter.
    def enterAlter(self, ctx:SqlBaseParser.AlterContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alter.
    def exitAlter(self, ctx:SqlBaseParser.AlterContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#resetGlobal.
    def enterResetGlobal(self, ctx:SqlBaseParser.ResetGlobalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#resetGlobal.
    def exitResetGlobal(self, ctx:SqlBaseParser.ResetGlobalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setTransaction.
    def enterSetTransaction(self, ctx:SqlBaseParser.SetTransactionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setTransaction.
    def exitSetTransaction(self, ctx:SqlBaseParser.SetTransactionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setSessionAuthorization.
    def enterSetSessionAuthorization(self, ctx:SqlBaseParser.SetSessionAuthorizationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setSessionAuthorization.
    def exitSetSessionAuthorization(self, ctx:SqlBaseParser.SetSessionAuthorizationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#resetSessionAuthorization.
    def enterResetSessionAuthorization(self, ctx:SqlBaseParser.ResetSessionAuthorizationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#resetSessionAuthorization.
    def exitResetSessionAuthorization(self, ctx:SqlBaseParser.ResetSessionAuthorizationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#set.
    def enterSet(self, ctx:SqlBaseParser.SetContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#set.
    def exitSet(self, ctx:SqlBaseParser.SetContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setGlobal.
    def enterSetGlobal(self, ctx:SqlBaseParser.SetGlobalContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setGlobal.
    def exitSetGlobal(self, ctx:SqlBaseParser.SetGlobalContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setTimeZone.
    def enterSetTimeZone(self, ctx:SqlBaseParser.SetTimeZoneContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setTimeZone.
    def exitSetTimeZone(self, ctx:SqlBaseParser.SetTimeZoneContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#kill.
    def enterKill(self, ctx:SqlBaseParser.KillContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#kill.
    def exitKill(self, ctx:SqlBaseParser.KillContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#insert.
    def enterInsert(self, ctx:SqlBaseParser.InsertContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#insert.
    def exitInsert(self, ctx:SqlBaseParser.InsertContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#restore.
    def enterRestore(self, ctx:SqlBaseParser.RestoreContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#restore.
    def exitRestore(self, ctx:SqlBaseParser.RestoreContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#copyFrom.
    def enterCopyFrom(self, ctx:SqlBaseParser.CopyFromContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#copyFrom.
    def exitCopyFrom(self, ctx:SqlBaseParser.CopyFromContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#copyTo.
    def enterCopyTo(self, ctx:SqlBaseParser.CopyToContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#copyTo.
    def exitCopyTo(self, ctx:SqlBaseParser.CopyToContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#drop.
    def enterDrop(self, ctx:SqlBaseParser.DropContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#drop.
    def exitDrop(self, ctx:SqlBaseParser.DropContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#grantPrivilege.
    def enterGrantPrivilege(self, ctx:SqlBaseParser.GrantPrivilegeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#grantPrivilege.
    def exitGrantPrivilege(self, ctx:SqlBaseParser.GrantPrivilegeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#denyPrivilege.
    def enterDenyPrivilege(self, ctx:SqlBaseParser.DenyPrivilegeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#denyPrivilege.
    def exitDenyPrivilege(self, ctx:SqlBaseParser.DenyPrivilegeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#revokePrivilege.
    def enterRevokePrivilege(self, ctx:SqlBaseParser.RevokePrivilegeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#revokePrivilege.
    def exitRevokePrivilege(self, ctx:SqlBaseParser.RevokePrivilegeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#create.
    def enterCreate(self, ctx:SqlBaseParser.CreateContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#create.
    def exitCreate(self, ctx:SqlBaseParser.CreateContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#deallocate.
    def enterDeallocate(self, ctx:SqlBaseParser.DeallocateContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#deallocate.
    def exitDeallocate(self, ctx:SqlBaseParser.DeallocateContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#analyze.
    def enterAnalyze(self, ctx:SqlBaseParser.AnalyzeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#analyze.
    def exitAnalyze(self, ctx:SqlBaseParser.AnalyzeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#discard.
    def enterDiscard(self, ctx:SqlBaseParser.DiscardContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#discard.
    def exitDiscard(self, ctx:SqlBaseParser.DiscardContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#declare.
    def enterDeclare(self, ctx:SqlBaseParser.DeclareContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#declare.
    def exitDeclare(self, ctx:SqlBaseParser.DeclareContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#fetch.
    def enterFetch(self, ctx:SqlBaseParser.FetchContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#fetch.
    def exitFetch(self, ctx:SqlBaseParser.FetchContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#close.
    def enterClose(self, ctx:SqlBaseParser.CloseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#close.
    def exitClose(self, ctx:SqlBaseParser.CloseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropBlobTable.
    def enterDropBlobTable(self, ctx:SqlBaseParser.DropBlobTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropBlobTable.
    def exitDropBlobTable(self, ctx:SqlBaseParser.DropBlobTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropTable.
    def enterDropTable(self, ctx:SqlBaseParser.DropTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropTable.
    def exitDropTable(self, ctx:SqlBaseParser.DropTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropAlias.
    def enterDropAlias(self, ctx:SqlBaseParser.DropAliasContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropAlias.
    def exitDropAlias(self, ctx:SqlBaseParser.DropAliasContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropRepository.
    def enterDropRepository(self, ctx:SqlBaseParser.DropRepositoryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropRepository.
    def exitDropRepository(self, ctx:SqlBaseParser.DropRepositoryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropSnapshot.
    def enterDropSnapshot(self, ctx:SqlBaseParser.DropSnapshotContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropSnapshot.
    def exitDropSnapshot(self, ctx:SqlBaseParser.DropSnapshotContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropFunction.
    def enterDropFunction(self, ctx:SqlBaseParser.DropFunctionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropFunction.
    def exitDropFunction(self, ctx:SqlBaseParser.DropFunctionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropRole.
    def enterDropRole(self, ctx:SqlBaseParser.DropRoleContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropRole.
    def exitDropRole(self, ctx:SqlBaseParser.DropRoleContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropView.
    def enterDropView(self, ctx:SqlBaseParser.DropViewContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropView.
    def exitDropView(self, ctx:SqlBaseParser.DropViewContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropAnalyzer.
    def enterDropAnalyzer(self, ctx:SqlBaseParser.DropAnalyzerContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropAnalyzer.
    def exitDropAnalyzer(self, ctx:SqlBaseParser.DropAnalyzerContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropPublication.
    def enterDropPublication(self, ctx:SqlBaseParser.DropPublicationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropPublication.
    def exitDropPublication(self, ctx:SqlBaseParser.DropPublicationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropSubscription.
    def enterDropSubscription(self, ctx:SqlBaseParser.DropSubscriptionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropSubscription.
    def exitDropSubscription(self, ctx:SqlBaseParser.DropSubscriptionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropServer.
    def enterDropServer(self, ctx:SqlBaseParser.DropServerContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropServer.
    def exitDropServer(self, ctx:SqlBaseParser.DropServerContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropForeignTable.
    def enterDropForeignTable(self, ctx:SqlBaseParser.DropForeignTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropForeignTable.
    def exitDropForeignTable(self, ctx:SqlBaseParser.DropForeignTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropUserMapping.
    def enterDropUserMapping(self, ctx:SqlBaseParser.DropUserMappingContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropUserMapping.
    def exitDropUserMapping(self, ctx:SqlBaseParser.DropUserMappingContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#addColumn.
    def enterAddColumn(self, ctx:SqlBaseParser.AddColumnContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#addColumn.
    def exitAddColumn(self, ctx:SqlBaseParser.AddColumnContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropColumn.
    def enterDropColumn(self, ctx:SqlBaseParser.DropColumnContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropColumn.
    def exitDropColumn(self, ctx:SqlBaseParser.DropColumnContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropCheckConstraint.
    def enterDropCheckConstraint(self, ctx:SqlBaseParser.DropCheckConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropCheckConstraint.
    def exitDropCheckConstraint(self, ctx:SqlBaseParser.DropCheckConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterTableProperties.
    def enterAlterTableProperties(self, ctx:SqlBaseParser.AlterTablePropertiesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterTableProperties.
    def exitAlterTableProperties(self, ctx:SqlBaseParser.AlterTablePropertiesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterBlobTableProperties.
    def enterAlterBlobTableProperties(self, ctx:SqlBaseParser.AlterBlobTablePropertiesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterBlobTableProperties.
    def exitAlterBlobTableProperties(self, ctx:SqlBaseParser.AlterBlobTablePropertiesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterTableOpenClose.
    def enterAlterTableOpenClose(self, ctx:SqlBaseParser.AlterTableOpenCloseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterTableOpenClose.
    def exitAlterTableOpenClose(self, ctx:SqlBaseParser.AlterTableOpenCloseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterTableRenameTable.
    def enterAlterTableRenameTable(self, ctx:SqlBaseParser.AlterTableRenameTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterTableRenameTable.
    def exitAlterTableRenameTable(self, ctx:SqlBaseParser.AlterTableRenameTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterTableRenameColumn.
    def enterAlterTableRenameColumn(self, ctx:SqlBaseParser.AlterTableRenameColumnContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterTableRenameColumn.
    def exitAlterTableRenameColumn(self, ctx:SqlBaseParser.AlterTableRenameColumnContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterTableReroute.
    def enterAlterTableReroute(self, ctx:SqlBaseParser.AlterTableRerouteContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterTableReroute.
    def exitAlterTableReroute(self, ctx:SqlBaseParser.AlterTableRerouteContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterClusterRerouteRetryFailed.
    def enterAlterClusterRerouteRetryFailed(self, ctx:SqlBaseParser.AlterClusterRerouteRetryFailedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterClusterRerouteRetryFailed.
    def exitAlterClusterRerouteRetryFailed(self, ctx:SqlBaseParser.AlterClusterRerouteRetryFailedContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterClusterSwapTable.
    def enterAlterClusterSwapTable(self, ctx:SqlBaseParser.AlterClusterSwapTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterClusterSwapTable.
    def exitAlterClusterSwapTable(self, ctx:SqlBaseParser.AlterClusterSwapTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterClusterDecommissionNode.
    def enterAlterClusterDecommissionNode(self, ctx:SqlBaseParser.AlterClusterDecommissionNodeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterClusterDecommissionNode.
    def exitAlterClusterDecommissionNode(self, ctx:SqlBaseParser.AlterClusterDecommissionNodeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterClusterGCDanglingArtifacts.
    def enterAlterClusterGCDanglingArtifacts(self, ctx:SqlBaseParser.AlterClusterGCDanglingArtifactsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterClusterGCDanglingArtifacts.
    def exitAlterClusterGCDanglingArtifacts(self, ctx:SqlBaseParser.AlterClusterGCDanglingArtifactsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterRoleSet.
    def enterAlterRoleSet(self, ctx:SqlBaseParser.AlterRoleSetContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterRoleSet.
    def exitAlterRoleSet(self, ctx:SqlBaseParser.AlterRoleSetContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterRoleReset.
    def enterAlterRoleReset(self, ctx:SqlBaseParser.AlterRoleResetContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterRoleReset.
    def exitAlterRoleReset(self, ctx:SqlBaseParser.AlterRoleResetContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterPublication.
    def enterAlterPublication(self, ctx:SqlBaseParser.AlterPublicationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterPublication.
    def exitAlterPublication(self, ctx:SqlBaseParser.AlterPublicationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterSubscription.
    def enterAlterSubscription(self, ctx:SqlBaseParser.AlterSubscriptionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterSubscription.
    def exitAlterSubscription(self, ctx:SqlBaseParser.AlterSubscriptionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterServer.
    def enterAlterServer(self, ctx:SqlBaseParser.AlterServerContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterServer.
    def exitAlterServer(self, ctx:SqlBaseParser.AlterServerContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#queryOptParens.
    def enterQueryOptParens(self, ctx:SqlBaseParser.QueryOptParensContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#queryOptParens.
    def exitQueryOptParens(self, ctx:SqlBaseParser.QueryOptParensContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#query.
    def enterQuery(self, ctx:SqlBaseParser.QueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#query.
    def exitQuery(self, ctx:SqlBaseParser.QueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#queryNoWith.
    def enterQueryNoWith(self, ctx:SqlBaseParser.QueryNoWithContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#queryNoWith.
    def exitQueryNoWith(self, ctx:SqlBaseParser.QueryNoWithContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#limitClause.
    def enterLimitClause(self, ctx:SqlBaseParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#limitClause.
    def exitLimitClause(self, ctx:SqlBaseParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#offsetClause.
    def enterOffsetClause(self, ctx:SqlBaseParser.OffsetClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#offsetClause.
    def exitOffsetClause(self, ctx:SqlBaseParser.OffsetClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#queryTermDefault.
    def enterQueryTermDefault(self, ctx:SqlBaseParser.QueryTermDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#queryTermDefault.
    def exitQueryTermDefault(self, ctx:SqlBaseParser.QueryTermDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setOperation.
    def enterSetOperation(self, ctx:SqlBaseParser.SetOperationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setOperation.
    def exitSetOperation(self, ctx:SqlBaseParser.SetOperationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setQuant.
    def enterSetQuant(self, ctx:SqlBaseParser.SetQuantContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setQuant.
    def exitSetQuant(self, ctx:SqlBaseParser.SetQuantContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#sortItem.
    def enterSortItem(self, ctx:SqlBaseParser.SortItemContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#sortItem.
    def exitSortItem(self, ctx:SqlBaseParser.SortItemContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#defaultQuerySpec.
    def enterDefaultQuerySpec(self, ctx:SqlBaseParser.DefaultQuerySpecContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#defaultQuerySpec.
    def exitDefaultQuerySpec(self, ctx:SqlBaseParser.DefaultQuerySpecContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#valuesRelation.
    def enterValuesRelation(self, ctx:SqlBaseParser.ValuesRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#valuesRelation.
    def exitValuesRelation(self, ctx:SqlBaseParser.ValuesRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#selectSingle.
    def enterSelectSingle(self, ctx:SqlBaseParser.SelectSingleContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#selectSingle.
    def exitSelectSingle(self, ctx:SqlBaseParser.SelectSingleContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#selectAll.
    def enterSelectAll(self, ctx:SqlBaseParser.SelectAllContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#selectAll.
    def exitSelectAll(self, ctx:SqlBaseParser.SelectAllContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#where.
    def enterWhere(self, ctx:SqlBaseParser.WhereContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#where.
    def exitWhere(self, ctx:SqlBaseParser.WhereContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#returning.
    def enterReturning(self, ctx:SqlBaseParser.ReturningContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#returning.
    def exitReturning(self, ctx:SqlBaseParser.ReturningContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#filter.
    def enterFilter(self, ctx:SqlBaseParser.FilterContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#filter.
    def exitFilter(self, ctx:SqlBaseParser.FilterContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#relationDefault.
    def enterRelationDefault(self, ctx:SqlBaseParser.RelationDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#relationDefault.
    def exitRelationDefault(self, ctx:SqlBaseParser.RelationDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#joinRelation.
    def enterJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#joinRelation.
    def exitJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#joinType.
    def enterJoinType(self, ctx:SqlBaseParser.JoinTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#joinType.
    def exitJoinType(self, ctx:SqlBaseParser.JoinTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#joinCriteria.
    def enterJoinCriteria(self, ctx:SqlBaseParser.JoinCriteriaContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#joinCriteria.
    def exitJoinCriteria(self, ctx:SqlBaseParser.JoinCriteriaContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#aliasedRelation.
    def enterAliasedRelation(self, ctx:SqlBaseParser.AliasedRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#aliasedRelation.
    def exitAliasedRelation(self, ctx:SqlBaseParser.AliasedRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableRelation.
    def enterTableRelation(self, ctx:SqlBaseParser.TableRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableRelation.
    def exitTableRelation(self, ctx:SqlBaseParser.TableRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subqueryRelation.
    def enterSubqueryRelation(self, ctx:SqlBaseParser.SubqueryRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subqueryRelation.
    def exitSubqueryRelation(self, ctx:SqlBaseParser.SubqueryRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parenthesizedRelation.
    def enterParenthesizedRelation(self, ctx:SqlBaseParser.ParenthesizedRelationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parenthesizedRelation.
    def exitParenthesizedRelation(self, ctx:SqlBaseParser.ParenthesizedRelationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableWithPartition.
    def enterTableWithPartition(self, ctx:SqlBaseParser.TableWithPartitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableWithPartition.
    def exitTableWithPartition(self, ctx:SqlBaseParser.TableWithPartitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableName.
    def enterTableName(self, ctx:SqlBaseParser.TableNameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableName.
    def exitTableName(self, ctx:SqlBaseParser.TableNameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableFunction.
    def enterTableFunction(self, ctx:SqlBaseParser.TableFunctionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableFunction.
    def exitTableFunction(self, ctx:SqlBaseParser.TableFunctionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#aliasedColumns.
    def enterAliasedColumns(self, ctx:SqlBaseParser.AliasedColumnsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#aliasedColumns.
    def exitAliasedColumns(self, ctx:SqlBaseParser.AliasedColumnsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#with.
    def enterWith(self, ctx:SqlBaseParser.WithContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#with.
    def exitWith(self, ctx:SqlBaseParser.WithContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedQuery.
    def enterNamedQuery(self, ctx:SqlBaseParser.NamedQueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedQuery.
    def exitNamedQuery(self, ctx:SqlBaseParser.NamedQueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#expr.
    def enterExpr(self, ctx:SqlBaseParser.ExprContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#expr.
    def exitExpr(self, ctx:SqlBaseParser.ExprContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#logicalNot.
    def enterLogicalNot(self, ctx:SqlBaseParser.LogicalNotContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#logicalNot.
    def exitLogicalNot(self, ctx:SqlBaseParser.LogicalNotContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#booleanDefault.
    def enterBooleanDefault(self, ctx:SqlBaseParser.BooleanDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#booleanDefault.
    def exitBooleanDefault(self, ctx:SqlBaseParser.BooleanDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#match.
    def enterMatch(self, ctx:SqlBaseParser.MatchContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#match.
    def exitMatch(self, ctx:SqlBaseParser.MatchContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#logicalBinary.
    def enterLogicalBinary(self, ctx:SqlBaseParser.LogicalBinaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#logicalBinary.
    def exitLogicalBinary(self, ctx:SqlBaseParser.LogicalBinaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#predicated.
    def enterPredicated(self, ctx:SqlBaseParser.PredicatedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#predicated.
    def exitPredicated(self, ctx:SqlBaseParser.PredicatedContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#comparison.
    def enterComparison(self, ctx:SqlBaseParser.ComparisonContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#comparison.
    def exitComparison(self, ctx:SqlBaseParser.ComparisonContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#quantifiedComparison.
    def enterQuantifiedComparison(self, ctx:SqlBaseParser.QuantifiedComparisonContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#quantifiedComparison.
    def exitQuantifiedComparison(self, ctx:SqlBaseParser.QuantifiedComparisonContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#between.
    def enterBetween(self, ctx:SqlBaseParser.BetweenContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#between.
    def exitBetween(self, ctx:SqlBaseParser.BetweenContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#inList.
    def enterInList(self, ctx:SqlBaseParser.InListContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#inList.
    def exitInList(self, ctx:SqlBaseParser.InListContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#inSubquery.
    def enterInSubquery(self, ctx:SqlBaseParser.InSubqueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#inSubquery.
    def exitInSubquery(self, ctx:SqlBaseParser.InSubqueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#like.
    def enterLike(self, ctx:SqlBaseParser.LikeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#like.
    def exitLike(self, ctx:SqlBaseParser.LikeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arrayLike.
    def enterArrayLike(self, ctx:SqlBaseParser.ArrayLikeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arrayLike.
    def exitArrayLike(self, ctx:SqlBaseParser.ArrayLikeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nullPredicate.
    def enterNullPredicate(self, ctx:SqlBaseParser.NullPredicateContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nullPredicate.
    def exitNullPredicate(self, ctx:SqlBaseParser.NullPredicateContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#distinctFrom.
    def enterDistinctFrom(self, ctx:SqlBaseParser.DistinctFromContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#distinctFrom.
    def exitDistinctFrom(self, ctx:SqlBaseParser.DistinctFromContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#bitwiseBinary.
    def enterBitwiseBinary(self, ctx:SqlBaseParser.BitwiseBinaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#bitwiseBinary.
    def exitBitwiseBinary(self, ctx:SqlBaseParser.BitwiseBinaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#valueExpressionDefault.
    def enterValueExpressionDefault(self, ctx:SqlBaseParser.ValueExpressionDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#valueExpressionDefault.
    def exitValueExpressionDefault(self, ctx:SqlBaseParser.ValueExpressionDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#concatenation.
    def enterConcatenation(self, ctx:SqlBaseParser.ConcatenationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#concatenation.
    def exitConcatenation(self, ctx:SqlBaseParser.ConcatenationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#overlap.
    def enterOverlap(self, ctx:SqlBaseParser.OverlapContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#overlap.
    def exitOverlap(self, ctx:SqlBaseParser.OverlapContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#fromStringLiteralCast.
    def enterFromStringLiteralCast(self, ctx:SqlBaseParser.FromStringLiteralCastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#fromStringLiteralCast.
    def exitFromStringLiteralCast(self, ctx:SqlBaseParser.FromStringLiteralCastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arithmeticBinary.
    def enterArithmeticBinary(self, ctx:SqlBaseParser.ArithmeticBinaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arithmeticBinary.
    def exitArithmeticBinary(self, ctx:SqlBaseParser.ArithmeticBinaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arithmeticUnary.
    def enterArithmeticUnary(self, ctx:SqlBaseParser.ArithmeticUnaryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arithmeticUnary.
    def exitArithmeticUnary(self, ctx:SqlBaseParser.ArithmeticUnaryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subqueryExpressionDefault.
    def enterSubqueryExpressionDefault(self, ctx:SqlBaseParser.SubqueryExpressionDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subqueryExpressionDefault.
    def exitSubqueryExpressionDefault(self, ctx:SqlBaseParser.SubqueryExpressionDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dereference.
    def enterDereference(self, ctx:SqlBaseParser.DereferenceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dereference.
    def exitDereference(self, ctx:SqlBaseParser.DereferenceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnReference.
    def enterColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnReference.
    def exitColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#atTimezone.
    def enterAtTimezone(self, ctx:SqlBaseParser.AtTimezoneContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#atTimezone.
    def exitAtTimezone(self, ctx:SqlBaseParser.AtTimezoneContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subscript.
    def enterSubscript(self, ctx:SqlBaseParser.SubscriptContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subscript.
    def exitSubscript(self, ctx:SqlBaseParser.SubscriptContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#recordSubscript.
    def enterRecordSubscript(self, ctx:SqlBaseParser.RecordSubscriptContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#recordSubscript.
    def exitRecordSubscript(self, ctx:SqlBaseParser.RecordSubscriptContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#explicitFunctionDefault.
    def enterExplicitFunctionDefault(self, ctx:SqlBaseParser.ExplicitFunctionDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#explicitFunctionDefault.
    def exitExplicitFunctionDefault(self, ctx:SqlBaseParser.ExplicitFunctionDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#doubleColonCast.
    def enterDoubleColonCast(self, ctx:SqlBaseParser.DoubleColonCastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#doubleColonCast.
    def exitDoubleColonCast(self, ctx:SqlBaseParser.DoubleColonCastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#defaultParamOrLiteral.
    def enterDefaultParamOrLiteral(self, ctx:SqlBaseParser.DefaultParamOrLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#defaultParamOrLiteral.
    def exitDefaultParamOrLiteral(self, ctx:SqlBaseParser.DefaultParamOrLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#functionCall.
    def enterFunctionCall(self, ctx:SqlBaseParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#functionCall.
    def exitFunctionCall(self, ctx:SqlBaseParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nestedExpression.
    def enterNestedExpression(self, ctx:SqlBaseParser.NestedExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nestedExpression.
    def exitNestedExpression(self, ctx:SqlBaseParser.NestedExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arraySlice.
    def enterArraySlice(self, ctx:SqlBaseParser.ArraySliceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arraySlice.
    def exitArraySlice(self, ctx:SqlBaseParser.ArraySliceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#exists.
    def enterExists(self, ctx:SqlBaseParser.ExistsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#exists.
    def exitExists(self, ctx:SqlBaseParser.ExistsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#emptyArray.
    def enterEmptyArray(self, ctx:SqlBaseParser.EmptyArrayContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#emptyArray.
    def exitEmptyArray(self, ctx:SqlBaseParser.EmptyArrayContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#specialDateTimeFunction.
    def enterSpecialDateTimeFunction(self, ctx:SqlBaseParser.SpecialDateTimeFunctionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#specialDateTimeFunction.
    def exitSpecialDateTimeFunction(self, ctx:SqlBaseParser.SpecialDateTimeFunctionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#currentCatalog.
    def enterCurrentCatalog(self, ctx:SqlBaseParser.CurrentCatalogContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#currentCatalog.
    def exitCurrentCatalog(self, ctx:SqlBaseParser.CurrentCatalogContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#currentSchema.
    def enterCurrentSchema(self, ctx:SqlBaseParser.CurrentSchemaContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#currentSchema.
    def exitCurrentSchema(self, ctx:SqlBaseParser.CurrentSchemaContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#currentUser.
    def enterCurrentUser(self, ctx:SqlBaseParser.CurrentUserContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#currentUser.
    def exitCurrentUser(self, ctx:SqlBaseParser.CurrentUserContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#sessionUser.
    def enterSessionUser(self, ctx:SqlBaseParser.SessionUserContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#sessionUser.
    def exitSessionUser(self, ctx:SqlBaseParser.SessionUserContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#left.
    def enterLeft(self, ctx:SqlBaseParser.LeftContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#left.
    def exitLeft(self, ctx:SqlBaseParser.LeftContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#right.
    def enterRight(self, ctx:SqlBaseParser.RightContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#right.
    def exitRight(self, ctx:SqlBaseParser.RightContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#substring.
    def enterSubstring(self, ctx:SqlBaseParser.SubstringContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#substring.
    def exitSubstring(self, ctx:SqlBaseParser.SubstringContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#position.
    def enterPosition(self, ctx:SqlBaseParser.PositionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#position.
    def exitPosition(self, ctx:SqlBaseParser.PositionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#trim.
    def enterTrim(self, ctx:SqlBaseParser.TrimContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#trim.
    def exitTrim(self, ctx:SqlBaseParser.TrimContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#extract.
    def enterExtract(self, ctx:SqlBaseParser.ExtractContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#extract.
    def exitExtract(self, ctx:SqlBaseParser.ExtractContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#cast.
    def enterCast(self, ctx:SqlBaseParser.CastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#cast.
    def exitCast(self, ctx:SqlBaseParser.CastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#simpleCase.
    def enterSimpleCase(self, ctx:SqlBaseParser.SimpleCaseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#simpleCase.
    def exitSimpleCase(self, ctx:SqlBaseParser.SimpleCaseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#searchedCase.
    def enterSearchedCase(self, ctx:SqlBaseParser.SearchedCaseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#searchedCase.
    def exitSearchedCase(self, ctx:SqlBaseParser.SearchedCaseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#ifCase.
    def enterIfCase(self, ctx:SqlBaseParser.IfCaseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#ifCase.
    def exitIfCase(self, ctx:SqlBaseParser.IfCaseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arraySubquery.
    def enterArraySubquery(self, ctx:SqlBaseParser.ArraySubqueryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arraySubquery.
    def exitArraySubquery(self, ctx:SqlBaseParser.ArraySubqueryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subqueryExpression.
    def enterSubqueryExpression(self, ctx:SqlBaseParser.SubqueryExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subqueryExpression.
    def exitSubqueryExpression(self, ctx:SqlBaseParser.SubqueryExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#simpleLiteral.
    def enterSimpleLiteral(self, ctx:SqlBaseParser.SimpleLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#simpleLiteral.
    def exitSimpleLiteral(self, ctx:SqlBaseParser.SimpleLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arrayLiteral.
    def enterArrayLiteral(self, ctx:SqlBaseParser.ArrayLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arrayLiteral.
    def exitArrayLiteral(self, ctx:SqlBaseParser.ArrayLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#objectLiteral.
    def enterObjectLiteral(self, ctx:SqlBaseParser.ObjectLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#objectLiteral.
    def exitObjectLiteral(self, ctx:SqlBaseParser.ObjectLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parameterOrSimpleLiteral.
    def enterParameterOrSimpleLiteral(self, ctx:SqlBaseParser.ParameterOrSimpleLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parameterOrSimpleLiteral.
    def exitParameterOrSimpleLiteral(self, ctx:SqlBaseParser.ParameterOrSimpleLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parameterExpression.
    def enterParameterExpression(self, ctx:SqlBaseParser.ParameterExpressionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parameterExpression.
    def exitParameterExpression(self, ctx:SqlBaseParser.ParameterExpressionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#intAsLiteral.
    def enterIntAsLiteral(self, ctx:SqlBaseParser.IntAsLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#intAsLiteral.
    def exitIntAsLiteral(self, ctx:SqlBaseParser.IntAsLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nullAsLiteral.
    def enterNullAsLiteral(self, ctx:SqlBaseParser.NullAsLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nullAsLiteral.
    def exitNullAsLiteral(self, ctx:SqlBaseParser.NullAsLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#integerParamOrLiteralDoubleColonCast.
    def enterIntegerParamOrLiteralDoubleColonCast(self, ctx:SqlBaseParser.IntegerParamOrLiteralDoubleColonCastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#integerParamOrLiteralDoubleColonCast.
    def exitIntegerParamOrLiteralDoubleColonCast(self, ctx:SqlBaseParser.IntegerParamOrLiteralDoubleColonCastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#integerParamOrLiteralCast.
    def enterIntegerParamOrLiteralCast(self, ctx:SqlBaseParser.IntegerParamOrLiteralCastContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#integerParamOrLiteralCast.
    def exitIntegerParamOrLiteralCast(self, ctx:SqlBaseParser.IntegerParamOrLiteralCastContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parameterOrIdent.
    def enterParameterOrIdent(self, ctx:SqlBaseParser.ParameterOrIdentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parameterOrIdent.
    def exitParameterOrIdent(self, ctx:SqlBaseParser.ParameterOrIdentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parameterOrString.
    def enterParameterOrString(self, ctx:SqlBaseParser.ParameterOrStringContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parameterOrString.
    def exitParameterOrString(self, ctx:SqlBaseParser.ParameterOrStringContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#positionalParameter.
    def enterPositionalParameter(self, ctx:SqlBaseParser.PositionalParameterContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#positionalParameter.
    def exitPositionalParameter(self, ctx:SqlBaseParser.PositionalParameterContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#parameterPlaceholder.
    def enterParameterPlaceholder(self, ctx:SqlBaseParser.ParameterPlaceholderContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#parameterPlaceholder.
    def exitParameterPlaceholder(self, ctx:SqlBaseParser.ParameterPlaceholderContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nullLiteral.
    def enterNullLiteral(self, ctx:SqlBaseParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nullLiteral.
    def exitNullLiteral(self, ctx:SqlBaseParser.NullLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#escapedCharsStringLiteral.
    def enterEscapedCharsStringLiteral(self, ctx:SqlBaseParser.EscapedCharsStringLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#escapedCharsStringLiteral.
    def exitEscapedCharsStringLiteral(self, ctx:SqlBaseParser.EscapedCharsStringLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dollarQuotedStringLiteral.
    def enterDollarQuotedStringLiteral(self, ctx:SqlBaseParser.DollarQuotedStringLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dollarQuotedStringLiteral.
    def exitDollarQuotedStringLiteral(self, ctx:SqlBaseParser.DollarQuotedStringLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#stringLiteral.
    def enterStringLiteral(self, ctx:SqlBaseParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#stringLiteral.
    def exitStringLiteral(self, ctx:SqlBaseParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#bitString.
    def enterBitString(self, ctx:SqlBaseParser.BitStringContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#bitString.
    def exitBitString(self, ctx:SqlBaseParser.BitStringContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#subscriptSafe.
    def enterSubscriptSafe(self, ctx:SqlBaseParser.SubscriptSafeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#subscriptSafe.
    def exitSubscriptSafe(self, ctx:SqlBaseParser.SubscriptSafeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#cmpOp.
    def enterCmpOp(self, ctx:SqlBaseParser.CmpOpContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#cmpOp.
    def exitCmpOp(self, ctx:SqlBaseParser.CmpOpContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setCmpQuantifier.
    def enterSetCmpQuantifier(self, ctx:SqlBaseParser.SetCmpQuantifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setCmpQuantifier.
    def exitSetCmpQuantifier(self, ctx:SqlBaseParser.SetCmpQuantifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#whenClause.
    def enterWhenClause(self, ctx:SqlBaseParser.WhenClauseContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#whenClause.
    def exitWhenClause(self, ctx:SqlBaseParser.WhenClauseContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedWindow.
    def enterNamedWindow(self, ctx:SqlBaseParser.NamedWindowContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedWindow.
    def exitNamedWindow(self, ctx:SqlBaseParser.NamedWindowContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#over.
    def enterOver(self, ctx:SqlBaseParser.OverContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#over.
    def exitOver(self, ctx:SqlBaseParser.OverContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#windowDefinition.
    def enterWindowDefinition(self, ctx:SqlBaseParser.WindowDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#windowDefinition.
    def exitWindowDefinition(self, ctx:SqlBaseParser.WindowDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#windowFrame.
    def enterWindowFrame(self, ctx:SqlBaseParser.WindowFrameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#windowFrame.
    def exitWindowFrame(self, ctx:SqlBaseParser.WindowFrameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#unboundedFrame.
    def enterUnboundedFrame(self, ctx:SqlBaseParser.UnboundedFrameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#unboundedFrame.
    def exitUnboundedFrame(self, ctx:SqlBaseParser.UnboundedFrameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#currentRowBound.
    def enterCurrentRowBound(self, ctx:SqlBaseParser.CurrentRowBoundContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#currentRowBound.
    def exitCurrentRowBound(self, ctx:SqlBaseParser.CurrentRowBoundContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#boundedFrame.
    def enterBoundedFrame(self, ctx:SqlBaseParser.BoundedFrameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#boundedFrame.
    def exitBoundedFrame(self, ctx:SqlBaseParser.BoundedFrameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#qnames.
    def enterQnames(self, ctx:SqlBaseParser.QnamesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#qnames.
    def exitQnames(self, ctx:SqlBaseParser.QnamesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#qname.
    def enterQname(self, ctx:SqlBaseParser.QnameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#qname.
    def exitQname(self, ctx:SqlBaseParser.QnameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#spaceSeparatedIdents.
    def enterSpaceSeparatedIdents(self, ctx:SqlBaseParser.SpaceSeparatedIdentsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#spaceSeparatedIdents.
    def exitSpaceSeparatedIdents(self, ctx:SqlBaseParser.SpaceSeparatedIdentsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#identWithOrWithoutValue.
    def enterIdentWithOrWithoutValue(self, ctx:SqlBaseParser.IdentWithOrWithoutValueContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#identWithOrWithoutValue.
    def exitIdentWithOrWithoutValue(self, ctx:SqlBaseParser.IdentWithOrWithoutValueContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#idents.
    def enterIdents(self, ctx:SqlBaseParser.IdentsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#idents.
    def exitIdents(self, ctx:SqlBaseParser.IdentsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#ident.
    def enterIdent(self, ctx:SqlBaseParser.IdentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#ident.
    def exitIdent(self, ctx:SqlBaseParser.IdentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#unquotedIdentifier.
    def enterUnquotedIdentifier(self, ctx:SqlBaseParser.UnquotedIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#unquotedIdentifier.
    def exitUnquotedIdentifier(self, ctx:SqlBaseParser.UnquotedIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#digitIdentifier.
    def enterDigitIdentifier(self, ctx:SqlBaseParser.DigitIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#digitIdentifier.
    def exitDigitIdentifier(self, ctx:SqlBaseParser.DigitIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#quotedIdentifier.
    def enterQuotedIdentifier(self, ctx:SqlBaseParser.QuotedIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#quotedIdentifier.
    def exitQuotedIdentifier(self, ctx:SqlBaseParser.QuotedIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#backQuotedIdentifier.
    def enterBackQuotedIdentifier(self, ctx:SqlBaseParser.BackQuotedIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#backQuotedIdentifier.
    def exitBackQuotedIdentifier(self, ctx:SqlBaseParser.BackQuotedIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#stringLiteralOrIdentifier.
    def enterStringLiteralOrIdentifier(self, ctx:SqlBaseParser.StringLiteralOrIdentifierContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#stringLiteralOrIdentifier.
    def exitStringLiteralOrIdentifier(self, ctx:SqlBaseParser.StringLiteralOrIdentifierContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#stringLiteralOrIdentifierOrQname.
    def enterStringLiteralOrIdentifierOrQname(self, ctx:SqlBaseParser.StringLiteralOrIdentifierOrQnameContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#stringLiteralOrIdentifierOrQname.
    def exitStringLiteralOrIdentifierOrQname(self, ctx:SqlBaseParser.StringLiteralOrIdentifierOrQnameContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#numericLiteral.
    def enterNumericLiteral(self, ctx:SqlBaseParser.NumericLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#numericLiteral.
    def exitNumericLiteral(self, ctx:SqlBaseParser.NumericLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#intervalLiteral.
    def enterIntervalLiteral(self, ctx:SqlBaseParser.IntervalLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#intervalLiteral.
    def exitIntervalLiteral(self, ctx:SqlBaseParser.IntervalLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#intervalField.
    def enterIntervalField(self, ctx:SqlBaseParser.IntervalFieldContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#intervalField.
    def exitIntervalField(self, ctx:SqlBaseParser.IntervalFieldContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:SqlBaseParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:SqlBaseParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#decimalLiteral.
    def enterDecimalLiteral(self, ctx:SqlBaseParser.DecimalLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#decimalLiteral.
    def exitDecimalLiteral(self, ctx:SqlBaseParser.DecimalLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#integerLiteral.
    def enterIntegerLiteral(self, ctx:SqlBaseParser.IntegerLiteralContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#integerLiteral.
    def exitIntegerLiteral(self, ctx:SqlBaseParser.IntegerLiteralContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#objectKeyValue.
    def enterObjectKeyValue(self, ctx:SqlBaseParser.ObjectKeyValueContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#objectKeyValue.
    def exitObjectKeyValue(self, ctx:SqlBaseParser.ObjectKeyValueContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#insertSource.
    def enterInsertSource(self, ctx:SqlBaseParser.InsertSourceContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#insertSource.
    def exitInsertSource(self, ctx:SqlBaseParser.InsertSourceContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#onConflict.
    def enterOnConflict(self, ctx:SqlBaseParser.OnConflictContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#onConflict.
    def exitOnConflict(self, ctx:SqlBaseParser.OnConflictContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#conflictTarget.
    def enterConflictTarget(self, ctx:SqlBaseParser.ConflictTargetContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#conflictTarget.
    def exitConflictTarget(self, ctx:SqlBaseParser.ConflictTargetContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#values.
    def enterValues(self, ctx:SqlBaseParser.ValuesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#values.
    def exitValues(self, ctx:SqlBaseParser.ValuesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columns.
    def enterColumns(self, ctx:SqlBaseParser.ColumnsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columns.
    def exitColumns(self, ctx:SqlBaseParser.ColumnsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#assignment.
    def enterAssignment(self, ctx:SqlBaseParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#assignment.
    def exitAssignment(self, ctx:SqlBaseParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createTable.
    def enterCreateTable(self, ctx:SqlBaseParser.CreateTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createTable.
    def exitCreateTable(self, ctx:SqlBaseParser.CreateTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createTableAs.
    def enterCreateTableAs(self, ctx:SqlBaseParser.CreateTableAsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createTableAs.
    def exitCreateTableAs(self, ctx:SqlBaseParser.CreateTableAsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createForeignTable.
    def enterCreateForeignTable(self, ctx:SqlBaseParser.CreateForeignTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createForeignTable.
    def exitCreateForeignTable(self, ctx:SqlBaseParser.CreateForeignTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createBlobTable.
    def enterCreateBlobTable(self, ctx:SqlBaseParser.CreateBlobTableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createBlobTable.
    def exitCreateBlobTable(self, ctx:SqlBaseParser.CreateBlobTableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createRepository.
    def enterCreateRepository(self, ctx:SqlBaseParser.CreateRepositoryContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createRepository.
    def exitCreateRepository(self, ctx:SqlBaseParser.CreateRepositoryContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createSnapshot.
    def enterCreateSnapshot(self, ctx:SqlBaseParser.CreateSnapshotContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createSnapshot.
    def exitCreateSnapshot(self, ctx:SqlBaseParser.CreateSnapshotContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createAnalyzer.
    def enterCreateAnalyzer(self, ctx:SqlBaseParser.CreateAnalyzerContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createAnalyzer.
    def exitCreateAnalyzer(self, ctx:SqlBaseParser.CreateAnalyzerContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createFunction.
    def enterCreateFunction(self, ctx:SqlBaseParser.CreateFunctionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createFunction.
    def exitCreateFunction(self, ctx:SqlBaseParser.CreateFunctionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createUserMapping.
    def enterCreateUserMapping(self, ctx:SqlBaseParser.CreateUserMappingContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createUserMapping.
    def exitCreateUserMapping(self, ctx:SqlBaseParser.CreateUserMappingContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createRole.
    def enterCreateRole(self, ctx:SqlBaseParser.CreateRoleContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createRole.
    def exitCreateRole(self, ctx:SqlBaseParser.CreateRoleContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createView.
    def enterCreateView(self, ctx:SqlBaseParser.CreateViewContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createView.
    def exitCreateView(self, ctx:SqlBaseParser.CreateViewContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createPublication.
    def enterCreatePublication(self, ctx:SqlBaseParser.CreatePublicationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createPublication.
    def exitCreatePublication(self, ctx:SqlBaseParser.CreatePublicationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createSubscription.
    def enterCreateSubscription(self, ctx:SqlBaseParser.CreateSubscriptionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createSubscription.
    def exitCreateSubscription(self, ctx:SqlBaseParser.CreateSubscriptionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#createServer.
    def enterCreateServer(self, ctx:SqlBaseParser.CreateServerContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#createServer.
    def exitCreateServer(self, ctx:SqlBaseParser.CreateServerContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#mappedUser.
    def enterMappedUser(self, ctx:SqlBaseParser.MappedUserContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#mappedUser.
    def exitMappedUser(self, ctx:SqlBaseParser.MappedUserContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#kvOptions.
    def enterKvOptions(self, ctx:SqlBaseParser.KvOptionsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#kvOptions.
    def exitKvOptions(self, ctx:SqlBaseParser.KvOptionsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#kvOption.
    def enterKvOption(self, ctx:SqlBaseParser.KvOptionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#kvOption.
    def exitKvOption(self, ctx:SqlBaseParser.KvOptionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterServerOptions.
    def enterAlterServerOptions(self, ctx:SqlBaseParser.AlterServerOptionsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterServerOptions.
    def exitAlterServerOptions(self, ctx:SqlBaseParser.AlterServerOptionsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#kvOptionWithOperation.
    def enterKvOptionWithOperation(self, ctx:SqlBaseParser.KvOptionWithOperationContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#kvOptionWithOperation.
    def exitKvOptionWithOperation(self, ctx:SqlBaseParser.KvOptionWithOperationContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#functionArgument.
    def enterFunctionArgument(self, ctx:SqlBaseParser.FunctionArgumentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#functionArgument.
    def exitFunctionArgument(self, ctx:SqlBaseParser.FunctionArgumentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableOnly.
    def enterTableOnly(self, ctx:SqlBaseParser.TableOnlyContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableOnly.
    def exitTableOnly(self, ctx:SqlBaseParser.TableOnlyContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableWithPartitionDefault.
    def enterTableWithPartitionDefault(self, ctx:SqlBaseParser.TableWithPartitionDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableWithPartitionDefault.
    def exitTableWithPartitionDefault(self, ctx:SqlBaseParser.TableWithPartitionDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#alterSubscriptionMode.
    def enterAlterSubscriptionMode(self, ctx:SqlBaseParser.AlterSubscriptionModeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#alterSubscriptionMode.
    def exitAlterSubscriptionMode(self, ctx:SqlBaseParser.AlterSubscriptionModeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#partitionedByOrClusteredInto.
    def enterPartitionedByOrClusteredInto(self, ctx:SqlBaseParser.PartitionedByOrClusteredIntoContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#partitionedByOrClusteredInto.
    def exitPartitionedByOrClusteredInto(self, ctx:SqlBaseParser.PartitionedByOrClusteredIntoContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#partitionedBy.
    def enterPartitionedBy(self, ctx:SqlBaseParser.PartitionedByContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#partitionedBy.
    def exitPartitionedBy(self, ctx:SqlBaseParser.PartitionedByContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#clusteredBy.
    def enterClusteredBy(self, ctx:SqlBaseParser.ClusteredByContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#clusteredBy.
    def exitClusteredBy(self, ctx:SqlBaseParser.ClusteredByContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#blobClusteredInto.
    def enterBlobClusteredInto(self, ctx:SqlBaseParser.BlobClusteredIntoContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#blobClusteredInto.
    def exitBlobClusteredInto(self, ctx:SqlBaseParser.BlobClusteredIntoContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnDefinitionDefault.
    def enterColumnDefinitionDefault(self, ctx:SqlBaseParser.ColumnDefinitionDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnDefinitionDefault.
    def exitColumnDefinitionDefault(self, ctx:SqlBaseParser.ColumnDefinitionDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#primaryKeyConstraintTableLevel.
    def enterPrimaryKeyConstraintTableLevel(self, ctx:SqlBaseParser.PrimaryKeyConstraintTableLevelContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#primaryKeyConstraintTableLevel.
    def exitPrimaryKeyConstraintTableLevel(self, ctx:SqlBaseParser.PrimaryKeyConstraintTableLevelContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#indexDefinition.
    def enterIndexDefinition(self, ctx:SqlBaseParser.IndexDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#indexDefinition.
    def exitIndexDefinition(self, ctx:SqlBaseParser.IndexDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableCheckConstraint.
    def enterTableCheckConstraint(self, ctx:SqlBaseParser.TableCheckConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableCheckConstraint.
    def exitTableCheckConstraint(self, ctx:SqlBaseParser.TableCheckConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnDefinition.
    def enterColumnDefinition(self, ctx:SqlBaseParser.ColumnDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnDefinition.
    def exitColumnDefinition(self, ctx:SqlBaseParser.ColumnDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#addColumnDefinition.
    def enterAddColumnDefinition(self, ctx:SqlBaseParser.AddColumnDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#addColumnDefinition.
    def exitAddColumnDefinition(self, ctx:SqlBaseParser.AddColumnDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#dropColumnDefinition.
    def enterDropColumnDefinition(self, ctx:SqlBaseParser.DropColumnDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#dropColumnDefinition.
    def exitDropColumnDefinition(self, ctx:SqlBaseParser.DropColumnDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#rerouteMoveShard.
    def enterRerouteMoveShard(self, ctx:SqlBaseParser.RerouteMoveShardContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#rerouteMoveShard.
    def exitRerouteMoveShard(self, ctx:SqlBaseParser.RerouteMoveShardContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#rerouteAllocateReplicaShard.
    def enterRerouteAllocateReplicaShard(self, ctx:SqlBaseParser.RerouteAllocateReplicaShardContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#rerouteAllocateReplicaShard.
    def exitRerouteAllocateReplicaShard(self, ctx:SqlBaseParser.RerouteAllocateReplicaShardContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#reroutePromoteReplica.
    def enterReroutePromoteReplica(self, ctx:SqlBaseParser.ReroutePromoteReplicaContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#reroutePromoteReplica.
    def exitReroutePromoteReplica(self, ctx:SqlBaseParser.ReroutePromoteReplicaContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#rerouteCancelShard.
    def enterRerouteCancelShard(self, ctx:SqlBaseParser.RerouteCancelShardContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#rerouteCancelShard.
    def exitRerouteCancelShard(self, ctx:SqlBaseParser.RerouteCancelShardContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#objectDataType.
    def enterObjectDataType(self, ctx:SqlBaseParser.ObjectDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#objectDataType.
    def exitObjectDataType(self, ctx:SqlBaseParser.ObjectDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#maybeParametrizedDataType.
    def enterMaybeParametrizedDataType(self, ctx:SqlBaseParser.MaybeParametrizedDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#maybeParametrizedDataType.
    def exitMaybeParametrizedDataType(self, ctx:SqlBaseParser.MaybeParametrizedDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#arrayDataType.
    def enterArrayDataType(self, ctx:SqlBaseParser.ArrayDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#arrayDataType.
    def exitArrayDataType(self, ctx:SqlBaseParser.ArrayDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#definedDataTypeDefault.
    def enterDefinedDataTypeDefault(self, ctx:SqlBaseParser.DefinedDataTypeDefaultContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#definedDataTypeDefault.
    def exitDefinedDataTypeDefault(self, ctx:SqlBaseParser.DefinedDataTypeDefaultContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#identDataType.
    def enterIdentDataType(self, ctx:SqlBaseParser.IdentDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#identDataType.
    def exitIdentDataType(self, ctx:SqlBaseParser.IdentDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#definedDataType.
    def enterDefinedDataType(self, ctx:SqlBaseParser.DefinedDataTypeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#definedDataType.
    def exitDefinedDataType(self, ctx:SqlBaseParser.DefinedDataTypeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#objectTypeDefinition.
    def enterObjectTypeDefinition(self, ctx:SqlBaseParser.ObjectTypeDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#objectTypeDefinition.
    def exitObjectTypeDefinition(self, ctx:SqlBaseParser.ObjectTypeDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnConstraintPrimaryKey.
    def enterColumnConstraintPrimaryKey(self, ctx:SqlBaseParser.ColumnConstraintPrimaryKeyContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnConstraintPrimaryKey.
    def exitColumnConstraintPrimaryKey(self, ctx:SqlBaseParser.ColumnConstraintPrimaryKeyContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnConstraintNotNull.
    def enterColumnConstraintNotNull(self, ctx:SqlBaseParser.ColumnConstraintNotNullContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnConstraintNotNull.
    def exitColumnConstraintNotNull(self, ctx:SqlBaseParser.ColumnConstraintNotNullContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnConstraintNull.
    def enterColumnConstraintNull(self, ctx:SqlBaseParser.ColumnConstraintNullContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnConstraintNull.
    def exitColumnConstraintNull(self, ctx:SqlBaseParser.ColumnConstraintNullContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnIndexConstraint.
    def enterColumnIndexConstraint(self, ctx:SqlBaseParser.ColumnIndexConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnIndexConstraint.
    def exitColumnIndexConstraint(self, ctx:SqlBaseParser.ColumnIndexConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnIndexOff.
    def enterColumnIndexOff(self, ctx:SqlBaseParser.ColumnIndexOffContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnIndexOff.
    def exitColumnIndexOff(self, ctx:SqlBaseParser.ColumnIndexOffContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnStorageDefinition.
    def enterColumnStorageDefinition(self, ctx:SqlBaseParser.ColumnStorageDefinitionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnStorageDefinition.
    def exitColumnStorageDefinition(self, ctx:SqlBaseParser.ColumnStorageDefinitionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnDefaultConstraint.
    def enterColumnDefaultConstraint(self, ctx:SqlBaseParser.ColumnDefaultConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnDefaultConstraint.
    def exitColumnDefaultConstraint(self, ctx:SqlBaseParser.ColumnDefaultConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnGeneratedConstraint.
    def enterColumnGeneratedConstraint(self, ctx:SqlBaseParser.ColumnGeneratedConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnGeneratedConstraint.
    def exitColumnGeneratedConstraint(self, ctx:SqlBaseParser.ColumnGeneratedConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#columnCheckConstraint.
    def enterColumnCheckConstraint(self, ctx:SqlBaseParser.ColumnCheckConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#columnCheckConstraint.
    def exitColumnCheckConstraint(self, ctx:SqlBaseParser.ColumnCheckConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#primaryKeyContraint.
    def enterPrimaryKeyContraint(self, ctx:SqlBaseParser.PrimaryKeyContraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#primaryKeyContraint.
    def exitPrimaryKeyContraint(self, ctx:SqlBaseParser.PrimaryKeyContraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#checkConstraint.
    def enterCheckConstraint(self, ctx:SqlBaseParser.CheckConstraintContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#checkConstraint.
    def exitCheckConstraint(self, ctx:SqlBaseParser.CheckConstraintContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#withGenericProperties.
    def enterWithGenericProperties(self, ctx:SqlBaseParser.WithGenericPropertiesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#withGenericProperties.
    def exitWithGenericProperties(self, ctx:SqlBaseParser.WithGenericPropertiesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#genericProperties.
    def enterGenericProperties(self, ctx:SqlBaseParser.GenericPropertiesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#genericProperties.
    def exitGenericProperties(self, ctx:SqlBaseParser.GenericPropertiesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#genericProperty.
    def enterGenericProperty(self, ctx:SqlBaseParser.GenericPropertyContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#genericProperty.
    def exitGenericProperty(self, ctx:SqlBaseParser.GenericPropertyContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#explainOptions.
    def enterExplainOptions(self, ctx:SqlBaseParser.ExplainOptionsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#explainOptions.
    def exitExplainOptions(self, ctx:SqlBaseParser.ExplainOptionsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#explainOption.
    def enterExplainOption(self, ctx:SqlBaseParser.ExplainOptionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#explainOption.
    def exitExplainOption(self, ctx:SqlBaseParser.ExplainOptionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#matchPredicateIdents.
    def enterMatchPredicateIdents(self, ctx:SqlBaseParser.MatchPredicateIdentsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#matchPredicateIdents.
    def exitMatchPredicateIdents(self, ctx:SqlBaseParser.MatchPredicateIdentsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#matchPredicateIdent.
    def enterMatchPredicateIdent(self, ctx:SqlBaseParser.MatchPredicateIdentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#matchPredicateIdent.
    def exitMatchPredicateIdent(self, ctx:SqlBaseParser.MatchPredicateIdentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#analyzerElement.
    def enterAnalyzerElement(self, ctx:SqlBaseParser.AnalyzerElementContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#analyzerElement.
    def exitAnalyzerElement(self, ctx:SqlBaseParser.AnalyzerElementContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tokenizer.
    def enterTokenizer(self, ctx:SqlBaseParser.TokenizerContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tokenizer.
    def exitTokenizer(self, ctx:SqlBaseParser.TokenizerContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tokenFilters.
    def enterTokenFilters(self, ctx:SqlBaseParser.TokenFiltersContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tokenFilters.
    def exitTokenFilters(self, ctx:SqlBaseParser.TokenFiltersContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#charFilters.
    def enterCharFilters(self, ctx:SqlBaseParser.CharFiltersContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#charFilters.
    def exitCharFilters(self, ctx:SqlBaseParser.CharFiltersContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#namedProperties.
    def enterNamedProperties(self, ctx:SqlBaseParser.NamedPropertiesContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#namedProperties.
    def exitNamedProperties(self, ctx:SqlBaseParser.NamedPropertiesContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#tableWithPartitions.
    def enterTableWithPartitions(self, ctx:SqlBaseParser.TableWithPartitionsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#tableWithPartitions.
    def exitTableWithPartitions(self, ctx:SqlBaseParser.TableWithPartitionsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setGlobalAssignment.
    def enterSetGlobalAssignment(self, ctx:SqlBaseParser.SetGlobalAssignmentContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setGlobalAssignment.
    def exitSetGlobalAssignment(self, ctx:SqlBaseParser.SetGlobalAssignmentContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#setExpr.
    def enterSetExpr(self, ctx:SqlBaseParser.SetExprContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#setExpr.
    def exitSetExpr(self, ctx:SqlBaseParser.SetExprContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#on.
    def enterOn(self, ctx:SqlBaseParser.OnContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#on.
    def exitOn(self, ctx:SqlBaseParser.OnContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#securable.
    def enterSecurable(self, ctx:SqlBaseParser.SecurableContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#securable.
    def exitSecurable(self, ctx:SqlBaseParser.SecurableContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#transactionMode.
    def enterTransactionMode(self, ctx:SqlBaseParser.TransactionModeContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#transactionMode.
    def exitTransactionMode(self, ctx:SqlBaseParser.TransactionModeContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#isolationLevel.
    def enterIsolationLevel(self, ctx:SqlBaseParser.IsolationLevelContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#isolationLevel.
    def exitIsolationLevel(self, ctx:SqlBaseParser.IsolationLevelContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#direction.
    def enterDirection(self, ctx:SqlBaseParser.DirectionContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#direction.
    def exitDirection(self, ctx:SqlBaseParser.DirectionContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#declareCursorParams.
    def enterDeclareCursorParams(self, ctx:SqlBaseParser.DeclareCursorParamsContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#declareCursorParams.
    def exitDeclareCursorParams(self, ctx:SqlBaseParser.DeclareCursorParamsContext):
        pass


    # Enter a parse tree produced by SqlBaseParser#nonReserved.
    def enterNonReserved(self, ctx:SqlBaseParser.NonReservedContext):
        pass

    # Exit a parse tree produced by SqlBaseParser#nonReserved.
    def exitNonReserved(self, ctx:SqlBaseParser.NonReservedContext):
        pass



del SqlBaseParser