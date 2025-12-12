# Generated from SqlBaseParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SqlBaseParser import SqlBaseParser
else:
    from SqlBaseParser import SqlBaseParser

# This class defines a complete generic visitor for a parse tree produced by SqlBaseParser.

class SqlBaseParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SqlBaseParser#statements.
    def visitStatements(self, ctx:SqlBaseParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#singleStatement.
    def visitSingleStatement(self, ctx:SqlBaseParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#singleExpression.
    def visitSingleExpression(self, ctx:SqlBaseParser.SingleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#default.
    def visitDefault(self, ctx:SqlBaseParser.DefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#begin.
    def visitBegin(self, ctx:SqlBaseParser.BeginContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#startTransaction.
    def visitStartTransaction(self, ctx:SqlBaseParser.StartTransactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#commit.
    def visitCommit(self, ctx:SqlBaseParser.CommitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#explain.
    def visitExplain(self, ctx:SqlBaseParser.ExplainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#optimize.
    def visitOptimize(self, ctx:SqlBaseParser.OptimizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#refreshTable.
    def visitRefreshTable(self, ctx:SqlBaseParser.RefreshTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#update.
    def visitUpdate(self, ctx:SqlBaseParser.UpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#delete.
    def visitDelete(self, ctx:SqlBaseParser.DeleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#showTransaction.
    def visitShowTransaction(self, ctx:SqlBaseParser.ShowTransactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#showCreateTable.
    def visitShowCreateTable(self, ctx:SqlBaseParser.ShowCreateTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#showTables.
    def visitShowTables(self, ctx:SqlBaseParser.ShowTablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#showSchemas.
    def visitShowSchemas(self, ctx:SqlBaseParser.ShowSchemasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#showColumns.
    def visitShowColumns(self, ctx:SqlBaseParser.ShowColumnsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#showSessionParameter.
    def visitShowSessionParameter(self, ctx:SqlBaseParser.ShowSessionParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alter.
    def visitAlter(self, ctx:SqlBaseParser.AlterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#resetGlobal.
    def visitResetGlobal(self, ctx:SqlBaseParser.ResetGlobalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setTransaction.
    def visitSetTransaction(self, ctx:SqlBaseParser.SetTransactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setSessionAuthorization.
    def visitSetSessionAuthorization(self, ctx:SqlBaseParser.SetSessionAuthorizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#resetSessionAuthorization.
    def visitResetSessionAuthorization(self, ctx:SqlBaseParser.ResetSessionAuthorizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#set.
    def visitSet(self, ctx:SqlBaseParser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setGlobal.
    def visitSetGlobal(self, ctx:SqlBaseParser.SetGlobalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setTimeZone.
    def visitSetTimeZone(self, ctx:SqlBaseParser.SetTimeZoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#kill.
    def visitKill(self, ctx:SqlBaseParser.KillContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#insert.
    def visitInsert(self, ctx:SqlBaseParser.InsertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#restore.
    def visitRestore(self, ctx:SqlBaseParser.RestoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#copyFrom.
    def visitCopyFrom(self, ctx:SqlBaseParser.CopyFromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#copyTo.
    def visitCopyTo(self, ctx:SqlBaseParser.CopyToContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#drop.
    def visitDrop(self, ctx:SqlBaseParser.DropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#grantPrivilege.
    def visitGrantPrivilege(self, ctx:SqlBaseParser.GrantPrivilegeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#denyPrivilege.
    def visitDenyPrivilege(self, ctx:SqlBaseParser.DenyPrivilegeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#revokePrivilege.
    def visitRevokePrivilege(self, ctx:SqlBaseParser.RevokePrivilegeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#create.
    def visitCreate(self, ctx:SqlBaseParser.CreateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#deallocate.
    def visitDeallocate(self, ctx:SqlBaseParser.DeallocateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#analyze.
    def visitAnalyze(self, ctx:SqlBaseParser.AnalyzeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#discard.
    def visitDiscard(self, ctx:SqlBaseParser.DiscardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#declare.
    def visitDeclare(self, ctx:SqlBaseParser.DeclareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#fetch.
    def visitFetch(self, ctx:SqlBaseParser.FetchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#close.
    def visitClose(self, ctx:SqlBaseParser.CloseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropBlobTable.
    def visitDropBlobTable(self, ctx:SqlBaseParser.DropBlobTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropTable.
    def visitDropTable(self, ctx:SqlBaseParser.DropTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropAlias.
    def visitDropAlias(self, ctx:SqlBaseParser.DropAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropRepository.
    def visitDropRepository(self, ctx:SqlBaseParser.DropRepositoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropSnapshot.
    def visitDropSnapshot(self, ctx:SqlBaseParser.DropSnapshotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropFunction.
    def visitDropFunction(self, ctx:SqlBaseParser.DropFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropRole.
    def visitDropRole(self, ctx:SqlBaseParser.DropRoleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropView.
    def visitDropView(self, ctx:SqlBaseParser.DropViewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropAnalyzer.
    def visitDropAnalyzer(self, ctx:SqlBaseParser.DropAnalyzerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropPublication.
    def visitDropPublication(self, ctx:SqlBaseParser.DropPublicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropSubscription.
    def visitDropSubscription(self, ctx:SqlBaseParser.DropSubscriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropServer.
    def visitDropServer(self, ctx:SqlBaseParser.DropServerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropForeignTable.
    def visitDropForeignTable(self, ctx:SqlBaseParser.DropForeignTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropUserMapping.
    def visitDropUserMapping(self, ctx:SqlBaseParser.DropUserMappingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#addColumn.
    def visitAddColumn(self, ctx:SqlBaseParser.AddColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropColumn.
    def visitDropColumn(self, ctx:SqlBaseParser.DropColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropCheckConstraint.
    def visitDropCheckConstraint(self, ctx:SqlBaseParser.DropCheckConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterTableProperties.
    def visitAlterTableProperties(self, ctx:SqlBaseParser.AlterTablePropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterBlobTableProperties.
    def visitAlterBlobTableProperties(self, ctx:SqlBaseParser.AlterBlobTablePropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterTableOpenClose.
    def visitAlterTableOpenClose(self, ctx:SqlBaseParser.AlterTableOpenCloseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterTableRenameTable.
    def visitAlterTableRenameTable(self, ctx:SqlBaseParser.AlterTableRenameTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterTableRenameColumn.
    def visitAlterTableRenameColumn(self, ctx:SqlBaseParser.AlterTableRenameColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterTableReroute.
    def visitAlterTableReroute(self, ctx:SqlBaseParser.AlterTableRerouteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterClusterRerouteRetryFailed.
    def visitAlterClusterRerouteRetryFailed(self, ctx:SqlBaseParser.AlterClusterRerouteRetryFailedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterClusterSwapTable.
    def visitAlterClusterSwapTable(self, ctx:SqlBaseParser.AlterClusterSwapTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterClusterDecommissionNode.
    def visitAlterClusterDecommissionNode(self, ctx:SqlBaseParser.AlterClusterDecommissionNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterClusterGCDanglingArtifacts.
    def visitAlterClusterGCDanglingArtifacts(self, ctx:SqlBaseParser.AlterClusterGCDanglingArtifactsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterRoleSet.
    def visitAlterRoleSet(self, ctx:SqlBaseParser.AlterRoleSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterRoleReset.
    def visitAlterRoleReset(self, ctx:SqlBaseParser.AlterRoleResetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterPublication.
    def visitAlterPublication(self, ctx:SqlBaseParser.AlterPublicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterSubscription.
    def visitAlterSubscription(self, ctx:SqlBaseParser.AlterSubscriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterServer.
    def visitAlterServer(self, ctx:SqlBaseParser.AlterServerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#queryOptParens.
    def visitQueryOptParens(self, ctx:SqlBaseParser.QueryOptParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#query.
    def visitQuery(self, ctx:SqlBaseParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#queryNoWith.
    def visitQueryNoWith(self, ctx:SqlBaseParser.QueryNoWithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#limitClause.
    def visitLimitClause(self, ctx:SqlBaseParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#offsetClause.
    def visitOffsetClause(self, ctx:SqlBaseParser.OffsetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#queryTermDefault.
    def visitQueryTermDefault(self, ctx:SqlBaseParser.QueryTermDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setOperation.
    def visitSetOperation(self, ctx:SqlBaseParser.SetOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setQuant.
    def visitSetQuant(self, ctx:SqlBaseParser.SetQuantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#sortItem.
    def visitSortItem(self, ctx:SqlBaseParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#defaultQuerySpec.
    def visitDefaultQuerySpec(self, ctx:SqlBaseParser.DefaultQuerySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#valuesRelation.
    def visitValuesRelation(self, ctx:SqlBaseParser.ValuesRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#selectSingle.
    def visitSelectSingle(self, ctx:SqlBaseParser.SelectSingleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#selectAll.
    def visitSelectAll(self, ctx:SqlBaseParser.SelectAllContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#where.
    def visitWhere(self, ctx:SqlBaseParser.WhereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#returning.
    def visitReturning(self, ctx:SqlBaseParser.ReturningContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#filter.
    def visitFilter(self, ctx:SqlBaseParser.FilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#relationDefault.
    def visitRelationDefault(self, ctx:SqlBaseParser.RelationDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#joinRelation.
    def visitJoinRelation(self, ctx:SqlBaseParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#joinType.
    def visitJoinType(self, ctx:SqlBaseParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#joinCriteria.
    def visitJoinCriteria(self, ctx:SqlBaseParser.JoinCriteriaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#aliasedRelation.
    def visitAliasedRelation(self, ctx:SqlBaseParser.AliasedRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableRelation.
    def visitTableRelation(self, ctx:SqlBaseParser.TableRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#subqueryRelation.
    def visitSubqueryRelation(self, ctx:SqlBaseParser.SubqueryRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#parenthesizedRelation.
    def visitParenthesizedRelation(self, ctx:SqlBaseParser.ParenthesizedRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableWithPartition.
    def visitTableWithPartition(self, ctx:SqlBaseParser.TableWithPartitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableName.
    def visitTableName(self, ctx:SqlBaseParser.TableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableFunction.
    def visitTableFunction(self, ctx:SqlBaseParser.TableFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#aliasedColumns.
    def visitAliasedColumns(self, ctx:SqlBaseParser.AliasedColumnsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#with.
    def visitWith(self, ctx:SqlBaseParser.WithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#namedQuery.
    def visitNamedQuery(self, ctx:SqlBaseParser.NamedQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#expr.
    def visitExpr(self, ctx:SqlBaseParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#logicalNot.
    def visitLogicalNot(self, ctx:SqlBaseParser.LogicalNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#booleanDefault.
    def visitBooleanDefault(self, ctx:SqlBaseParser.BooleanDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#match.
    def visitMatch(self, ctx:SqlBaseParser.MatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#logicalBinary.
    def visitLogicalBinary(self, ctx:SqlBaseParser.LogicalBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#predicated.
    def visitPredicated(self, ctx:SqlBaseParser.PredicatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#comparison.
    def visitComparison(self, ctx:SqlBaseParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#quantifiedComparison.
    def visitQuantifiedComparison(self, ctx:SqlBaseParser.QuantifiedComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#between.
    def visitBetween(self, ctx:SqlBaseParser.BetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#inList.
    def visitInList(self, ctx:SqlBaseParser.InListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#inSubquery.
    def visitInSubquery(self, ctx:SqlBaseParser.InSubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#like.
    def visitLike(self, ctx:SqlBaseParser.LikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arrayLike.
    def visitArrayLike(self, ctx:SqlBaseParser.ArrayLikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#nullPredicate.
    def visitNullPredicate(self, ctx:SqlBaseParser.NullPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#distinctFrom.
    def visitDistinctFrom(self, ctx:SqlBaseParser.DistinctFromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#bitwiseBinary.
    def visitBitwiseBinary(self, ctx:SqlBaseParser.BitwiseBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#valueExpressionDefault.
    def visitValueExpressionDefault(self, ctx:SqlBaseParser.ValueExpressionDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#concatenation.
    def visitConcatenation(self, ctx:SqlBaseParser.ConcatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#overlap.
    def visitOverlap(self, ctx:SqlBaseParser.OverlapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#fromStringLiteralCast.
    def visitFromStringLiteralCast(self, ctx:SqlBaseParser.FromStringLiteralCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arithmeticBinary.
    def visitArithmeticBinary(self, ctx:SqlBaseParser.ArithmeticBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arithmeticUnary.
    def visitArithmeticUnary(self, ctx:SqlBaseParser.ArithmeticUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#subqueryExpressionDefault.
    def visitSubqueryExpressionDefault(self, ctx:SqlBaseParser.SubqueryExpressionDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dereference.
    def visitDereference(self, ctx:SqlBaseParser.DereferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnReference.
    def visitColumnReference(self, ctx:SqlBaseParser.ColumnReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#atTimezone.
    def visitAtTimezone(self, ctx:SqlBaseParser.AtTimezoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#subscript.
    def visitSubscript(self, ctx:SqlBaseParser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#recordSubscript.
    def visitRecordSubscript(self, ctx:SqlBaseParser.RecordSubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#explicitFunctionDefault.
    def visitExplicitFunctionDefault(self, ctx:SqlBaseParser.ExplicitFunctionDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#doubleColonCast.
    def visitDoubleColonCast(self, ctx:SqlBaseParser.DoubleColonCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#defaultParamOrLiteral.
    def visitDefaultParamOrLiteral(self, ctx:SqlBaseParser.DefaultParamOrLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#functionCall.
    def visitFunctionCall(self, ctx:SqlBaseParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#nestedExpression.
    def visitNestedExpression(self, ctx:SqlBaseParser.NestedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arraySlice.
    def visitArraySlice(self, ctx:SqlBaseParser.ArraySliceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#exists.
    def visitExists(self, ctx:SqlBaseParser.ExistsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#emptyArray.
    def visitEmptyArray(self, ctx:SqlBaseParser.EmptyArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#specialDateTimeFunction.
    def visitSpecialDateTimeFunction(self, ctx:SqlBaseParser.SpecialDateTimeFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#currentCatalog.
    def visitCurrentCatalog(self, ctx:SqlBaseParser.CurrentCatalogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#currentSchema.
    def visitCurrentSchema(self, ctx:SqlBaseParser.CurrentSchemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#currentUser.
    def visitCurrentUser(self, ctx:SqlBaseParser.CurrentUserContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#sessionUser.
    def visitSessionUser(self, ctx:SqlBaseParser.SessionUserContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#left.
    def visitLeft(self, ctx:SqlBaseParser.LeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#right.
    def visitRight(self, ctx:SqlBaseParser.RightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#substring.
    def visitSubstring(self, ctx:SqlBaseParser.SubstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#position.
    def visitPosition(self, ctx:SqlBaseParser.PositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#trim.
    def visitTrim(self, ctx:SqlBaseParser.TrimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#extract.
    def visitExtract(self, ctx:SqlBaseParser.ExtractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#cast.
    def visitCast(self, ctx:SqlBaseParser.CastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#simpleCase.
    def visitSimpleCase(self, ctx:SqlBaseParser.SimpleCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#searchedCase.
    def visitSearchedCase(self, ctx:SqlBaseParser.SearchedCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#ifCase.
    def visitIfCase(self, ctx:SqlBaseParser.IfCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arraySubquery.
    def visitArraySubquery(self, ctx:SqlBaseParser.ArraySubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#subqueryExpression.
    def visitSubqueryExpression(self, ctx:SqlBaseParser.SubqueryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#simpleLiteral.
    def visitSimpleLiteral(self, ctx:SqlBaseParser.SimpleLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arrayLiteral.
    def visitArrayLiteral(self, ctx:SqlBaseParser.ArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#objectLiteral.
    def visitObjectLiteral(self, ctx:SqlBaseParser.ObjectLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#parameterOrSimpleLiteral.
    def visitParameterOrSimpleLiteral(self, ctx:SqlBaseParser.ParameterOrSimpleLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#parameterExpression.
    def visitParameterExpression(self, ctx:SqlBaseParser.ParameterExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#intAsLiteral.
    def visitIntAsLiteral(self, ctx:SqlBaseParser.IntAsLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#nullAsLiteral.
    def visitNullAsLiteral(self, ctx:SqlBaseParser.NullAsLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#integerParamOrLiteralDoubleColonCast.
    def visitIntegerParamOrLiteralDoubleColonCast(self, ctx:SqlBaseParser.IntegerParamOrLiteralDoubleColonCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#integerParamOrLiteralCast.
    def visitIntegerParamOrLiteralCast(self, ctx:SqlBaseParser.IntegerParamOrLiteralCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#parameterOrIdent.
    def visitParameterOrIdent(self, ctx:SqlBaseParser.ParameterOrIdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#parameterOrString.
    def visitParameterOrString(self, ctx:SqlBaseParser.ParameterOrStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#positionalParameter.
    def visitPositionalParameter(self, ctx:SqlBaseParser.PositionalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#parameterPlaceholder.
    def visitParameterPlaceholder(self, ctx:SqlBaseParser.ParameterPlaceholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#nullLiteral.
    def visitNullLiteral(self, ctx:SqlBaseParser.NullLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#escapedCharsStringLiteral.
    def visitEscapedCharsStringLiteral(self, ctx:SqlBaseParser.EscapedCharsStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dollarQuotedStringLiteral.
    def visitDollarQuotedStringLiteral(self, ctx:SqlBaseParser.DollarQuotedStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#stringLiteral.
    def visitStringLiteral(self, ctx:SqlBaseParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#bitString.
    def visitBitString(self, ctx:SqlBaseParser.BitStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#subscriptSafe.
    def visitSubscriptSafe(self, ctx:SqlBaseParser.SubscriptSafeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#cmpOp.
    def visitCmpOp(self, ctx:SqlBaseParser.CmpOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setCmpQuantifier.
    def visitSetCmpQuantifier(self, ctx:SqlBaseParser.SetCmpQuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#whenClause.
    def visitWhenClause(self, ctx:SqlBaseParser.WhenClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#namedWindow.
    def visitNamedWindow(self, ctx:SqlBaseParser.NamedWindowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#over.
    def visitOver(self, ctx:SqlBaseParser.OverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#windowDefinition.
    def visitWindowDefinition(self, ctx:SqlBaseParser.WindowDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#windowFrame.
    def visitWindowFrame(self, ctx:SqlBaseParser.WindowFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#unboundedFrame.
    def visitUnboundedFrame(self, ctx:SqlBaseParser.UnboundedFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#currentRowBound.
    def visitCurrentRowBound(self, ctx:SqlBaseParser.CurrentRowBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#boundedFrame.
    def visitBoundedFrame(self, ctx:SqlBaseParser.BoundedFrameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#qnames.
    def visitQnames(self, ctx:SqlBaseParser.QnamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#qname.
    def visitQname(self, ctx:SqlBaseParser.QnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#spaceSeparatedIdents.
    def visitSpaceSeparatedIdents(self, ctx:SqlBaseParser.SpaceSeparatedIdentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#identWithOrWithoutValue.
    def visitIdentWithOrWithoutValue(self, ctx:SqlBaseParser.IdentWithOrWithoutValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#idents.
    def visitIdents(self, ctx:SqlBaseParser.IdentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#ident.
    def visitIdent(self, ctx:SqlBaseParser.IdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#unquotedIdentifier.
    def visitUnquotedIdentifier(self, ctx:SqlBaseParser.UnquotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#digitIdentifier.
    def visitDigitIdentifier(self, ctx:SqlBaseParser.DigitIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#quotedIdentifier.
    def visitQuotedIdentifier(self, ctx:SqlBaseParser.QuotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#backQuotedIdentifier.
    def visitBackQuotedIdentifier(self, ctx:SqlBaseParser.BackQuotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#stringLiteralOrIdentifier.
    def visitStringLiteralOrIdentifier(self, ctx:SqlBaseParser.StringLiteralOrIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#stringLiteralOrIdentifierOrQname.
    def visitStringLiteralOrIdentifierOrQname(self, ctx:SqlBaseParser.StringLiteralOrIdentifierOrQnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#numericLiteral.
    def visitNumericLiteral(self, ctx:SqlBaseParser.NumericLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#intervalLiteral.
    def visitIntervalLiteral(self, ctx:SqlBaseParser.IntervalLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#intervalField.
    def visitIntervalField(self, ctx:SqlBaseParser.IntervalFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:SqlBaseParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#decimalLiteral.
    def visitDecimalLiteral(self, ctx:SqlBaseParser.DecimalLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#integerLiteral.
    def visitIntegerLiteral(self, ctx:SqlBaseParser.IntegerLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#objectKeyValue.
    def visitObjectKeyValue(self, ctx:SqlBaseParser.ObjectKeyValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#insertSource.
    def visitInsertSource(self, ctx:SqlBaseParser.InsertSourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#onConflict.
    def visitOnConflict(self, ctx:SqlBaseParser.OnConflictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#conflictTarget.
    def visitConflictTarget(self, ctx:SqlBaseParser.ConflictTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#values.
    def visitValues(self, ctx:SqlBaseParser.ValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columns.
    def visitColumns(self, ctx:SqlBaseParser.ColumnsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#assignment.
    def visitAssignment(self, ctx:SqlBaseParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createTable.
    def visitCreateTable(self, ctx:SqlBaseParser.CreateTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createTableAs.
    def visitCreateTableAs(self, ctx:SqlBaseParser.CreateTableAsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createForeignTable.
    def visitCreateForeignTable(self, ctx:SqlBaseParser.CreateForeignTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createBlobTable.
    def visitCreateBlobTable(self, ctx:SqlBaseParser.CreateBlobTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createRepository.
    def visitCreateRepository(self, ctx:SqlBaseParser.CreateRepositoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createSnapshot.
    def visitCreateSnapshot(self, ctx:SqlBaseParser.CreateSnapshotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createAnalyzer.
    def visitCreateAnalyzer(self, ctx:SqlBaseParser.CreateAnalyzerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createFunction.
    def visitCreateFunction(self, ctx:SqlBaseParser.CreateFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createUserMapping.
    def visitCreateUserMapping(self, ctx:SqlBaseParser.CreateUserMappingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createRole.
    def visitCreateRole(self, ctx:SqlBaseParser.CreateRoleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createView.
    def visitCreateView(self, ctx:SqlBaseParser.CreateViewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createPublication.
    def visitCreatePublication(self, ctx:SqlBaseParser.CreatePublicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createSubscription.
    def visitCreateSubscription(self, ctx:SqlBaseParser.CreateSubscriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#createServer.
    def visitCreateServer(self, ctx:SqlBaseParser.CreateServerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#mappedUser.
    def visitMappedUser(self, ctx:SqlBaseParser.MappedUserContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#kvOptions.
    def visitKvOptions(self, ctx:SqlBaseParser.KvOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#kvOption.
    def visitKvOption(self, ctx:SqlBaseParser.KvOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterServerOptions.
    def visitAlterServerOptions(self, ctx:SqlBaseParser.AlterServerOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#kvOptionWithOperation.
    def visitKvOptionWithOperation(self, ctx:SqlBaseParser.KvOptionWithOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#functionArgument.
    def visitFunctionArgument(self, ctx:SqlBaseParser.FunctionArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableOnly.
    def visitTableOnly(self, ctx:SqlBaseParser.TableOnlyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableWithPartitionDefault.
    def visitTableWithPartitionDefault(self, ctx:SqlBaseParser.TableWithPartitionDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#alterSubscriptionMode.
    def visitAlterSubscriptionMode(self, ctx:SqlBaseParser.AlterSubscriptionModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#partitionedByOrClusteredInto.
    def visitPartitionedByOrClusteredInto(self, ctx:SqlBaseParser.PartitionedByOrClusteredIntoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#partitionedBy.
    def visitPartitionedBy(self, ctx:SqlBaseParser.PartitionedByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#clusteredBy.
    def visitClusteredBy(self, ctx:SqlBaseParser.ClusteredByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#blobClusteredInto.
    def visitBlobClusteredInto(self, ctx:SqlBaseParser.BlobClusteredIntoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnDefinitionDefault.
    def visitColumnDefinitionDefault(self, ctx:SqlBaseParser.ColumnDefinitionDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#primaryKeyConstraintTableLevel.
    def visitPrimaryKeyConstraintTableLevel(self, ctx:SqlBaseParser.PrimaryKeyConstraintTableLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#indexDefinition.
    def visitIndexDefinition(self, ctx:SqlBaseParser.IndexDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableCheckConstraint.
    def visitTableCheckConstraint(self, ctx:SqlBaseParser.TableCheckConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnDefinition.
    def visitColumnDefinition(self, ctx:SqlBaseParser.ColumnDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#addColumnDefinition.
    def visitAddColumnDefinition(self, ctx:SqlBaseParser.AddColumnDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#dropColumnDefinition.
    def visitDropColumnDefinition(self, ctx:SqlBaseParser.DropColumnDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#rerouteMoveShard.
    def visitRerouteMoveShard(self, ctx:SqlBaseParser.RerouteMoveShardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#rerouteAllocateReplicaShard.
    def visitRerouteAllocateReplicaShard(self, ctx:SqlBaseParser.RerouteAllocateReplicaShardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#reroutePromoteReplica.
    def visitReroutePromoteReplica(self, ctx:SqlBaseParser.ReroutePromoteReplicaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#rerouteCancelShard.
    def visitRerouteCancelShard(self, ctx:SqlBaseParser.RerouteCancelShardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#objectDataType.
    def visitObjectDataType(self, ctx:SqlBaseParser.ObjectDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#maybeParametrizedDataType.
    def visitMaybeParametrizedDataType(self, ctx:SqlBaseParser.MaybeParametrizedDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#arrayDataType.
    def visitArrayDataType(self, ctx:SqlBaseParser.ArrayDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#definedDataTypeDefault.
    def visitDefinedDataTypeDefault(self, ctx:SqlBaseParser.DefinedDataTypeDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#identDataType.
    def visitIdentDataType(self, ctx:SqlBaseParser.IdentDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#definedDataType.
    def visitDefinedDataType(self, ctx:SqlBaseParser.DefinedDataTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#objectTypeDefinition.
    def visitObjectTypeDefinition(self, ctx:SqlBaseParser.ObjectTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnConstraintPrimaryKey.
    def visitColumnConstraintPrimaryKey(self, ctx:SqlBaseParser.ColumnConstraintPrimaryKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnConstraintNotNull.
    def visitColumnConstraintNotNull(self, ctx:SqlBaseParser.ColumnConstraintNotNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnConstraintNull.
    def visitColumnConstraintNull(self, ctx:SqlBaseParser.ColumnConstraintNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnIndexConstraint.
    def visitColumnIndexConstraint(self, ctx:SqlBaseParser.ColumnIndexConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnIndexOff.
    def visitColumnIndexOff(self, ctx:SqlBaseParser.ColumnIndexOffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnStorageDefinition.
    def visitColumnStorageDefinition(self, ctx:SqlBaseParser.ColumnStorageDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnDefaultConstraint.
    def visitColumnDefaultConstraint(self, ctx:SqlBaseParser.ColumnDefaultConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnGeneratedConstraint.
    def visitColumnGeneratedConstraint(self, ctx:SqlBaseParser.ColumnGeneratedConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#columnCheckConstraint.
    def visitColumnCheckConstraint(self, ctx:SqlBaseParser.ColumnCheckConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#primaryKeyContraint.
    def visitPrimaryKeyContraint(self, ctx:SqlBaseParser.PrimaryKeyContraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#checkConstraint.
    def visitCheckConstraint(self, ctx:SqlBaseParser.CheckConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#withGenericProperties.
    def visitWithGenericProperties(self, ctx:SqlBaseParser.WithGenericPropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#genericProperties.
    def visitGenericProperties(self, ctx:SqlBaseParser.GenericPropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#genericProperty.
    def visitGenericProperty(self, ctx:SqlBaseParser.GenericPropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#explainOptions.
    def visitExplainOptions(self, ctx:SqlBaseParser.ExplainOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#explainOption.
    def visitExplainOption(self, ctx:SqlBaseParser.ExplainOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#matchPredicateIdents.
    def visitMatchPredicateIdents(self, ctx:SqlBaseParser.MatchPredicateIdentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#matchPredicateIdent.
    def visitMatchPredicateIdent(self, ctx:SqlBaseParser.MatchPredicateIdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#analyzerElement.
    def visitAnalyzerElement(self, ctx:SqlBaseParser.AnalyzerElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tokenizer.
    def visitTokenizer(self, ctx:SqlBaseParser.TokenizerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tokenFilters.
    def visitTokenFilters(self, ctx:SqlBaseParser.TokenFiltersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#charFilters.
    def visitCharFilters(self, ctx:SqlBaseParser.CharFiltersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#namedProperties.
    def visitNamedProperties(self, ctx:SqlBaseParser.NamedPropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#tableWithPartitions.
    def visitTableWithPartitions(self, ctx:SqlBaseParser.TableWithPartitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setGlobalAssignment.
    def visitSetGlobalAssignment(self, ctx:SqlBaseParser.SetGlobalAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#setExpr.
    def visitSetExpr(self, ctx:SqlBaseParser.SetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#on.
    def visitOn(self, ctx:SqlBaseParser.OnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#securable.
    def visitSecurable(self, ctx:SqlBaseParser.SecurableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#transactionMode.
    def visitTransactionMode(self, ctx:SqlBaseParser.TransactionModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#isolationLevel.
    def visitIsolationLevel(self, ctx:SqlBaseParser.IsolationLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#direction.
    def visitDirection(self, ctx:SqlBaseParser.DirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#declareCursorParams.
    def visitDeclareCursorParams(self, ctx:SqlBaseParser.DeclareCursorParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SqlBaseParser#nonReserved.
    def visitNonReserved(self, ctx:SqlBaseParser.NonReservedContext):
        return self.visitChildren(ctx)



del SqlBaseParser